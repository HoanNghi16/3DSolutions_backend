from datetime import timedelta
from multiprocessing.context import AuthenticationError

from django.utils import timezone
from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView
from django.db.models import F

from carts_management.models import CartHeaders, CartDetails
from carts_management.serializer import CartDetailsSerializer
from products_management.models import Products
from products_management.serializer import ProductsSerializer
from users_management.authenticate import CookieAuthenticateJWT
from users_management.models import Address
from .data_processing import for_pie_chart, for_line_chart, for_bar_chart_1
from .models import OrderHeaders, OrderDetails
from .serializer import OrdersSerializer, OrderDetailsSerializer, OrdersListSerializer, ValidOrderHeader


# Create your views here.
class OrdersView(ListAPIView):
    serializer_class = OrdersListSerializer
    authentication_classes = [CookieAuthenticateJWT]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user.profile
        status = self.request.query_params.get('status')
        if status != 'null' and status:
            orders = OrderHeaders.objects.filter(user=user, order_status = int(status)).order_by('-date')
        else:
            orders = OrderHeaders.objects.filter(user=user).order_by('-date')
        return orders

class OrderDetailsView(RetrieveAPIView):
    serializer_class = OrdersSerializer
    authentication_classes = [CookieAuthenticateJWT]
    lookup_field = 'id'
    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return OrderHeaders.objects.all().order_by('-date')
            return OrderHeaders.objects.filter(user=self.request.user.profile).order_by('-date')
        else:
            return OrderHeaders.objects.filter(user=None).order_by('-date')


class OrderCreateView(APIView):
    authentication_classes = [CookieAuthenticateJWT]
    def post(self, request):
        try:
            with transaction.atomic():
                details = request.data.get('details', None)
                if not details:
                    raise Exception('Order must has at least one product')
                user = request.user.profile if request.user.is_authenticated else None
                method = int(request.data['header'].get('method',None))
                if method is None:
                    raise Exception('Vui lòng chọn phương thức thanh toán!')
                if method == 1:
                    pay_status = -1
                    expire_at = timezone.now() + timedelta(hours=1)
                else:
                    pay_status = 0
                    expire_at = None
                if user:
                    address_id = request.data['header'].get('address_id', None)
                    address = Address.objects.get(id=address_id, user= user)
                    if not address:
                        raise ValidationError('Address not found')
                    receiver_name = address.receiver_name
                    receiver_phone = address.receiver_phone
                    number = address.number
                    street = address.street
                    city = address.city
                    ward = address.ward
                else:
                    receiver_name = request.data['header'].get('receiver_name')
                    receiver_phone = request.data['header'].get('receiver_phone')
                    number = request.data['header'].get('number')
                    street = request.data['header'].get('street')
                    city = request.data['header'].get('city')
                    ward = request.data['header'].get('ward')
                print(city)
                header = OrderHeaders.objects.create(user=user, method=method, pay_status=pay_status, order_status=0, receiver_name=receiver_name,
                                                     receiver_phone=receiver_phone, number=number, street=street,
                                                     city=city, ward=ward, total = 0, expire_at = expire_at)
                total = 0.0
                for detail in details:
                    product = Products.objects.select_for_update().get(id=detail['product'])
                    quantity = int(detail['quantity'])
                    if (product.quantity < quantity):
                        raise ValidationError('Out stock')
                    product.quantity = F('quantity') - quantity
                    product.save()
                    term = OrderDetails.objects.create(header = header, product = product, quantity = quantity, current_price = product.unit_price)
                    total += term.quantity*term.current_price
                    term.save()
                header.total = total
                header.save()
                list_ids = request.data.get('list_ids', None)
                if list_ids and user:
                    cart_header = CartHeaders.objects.get(account = request.user if request.user.is_authenticated else None)
                    if cart_header:
                        CartDetails.objects.filter( id__in = list_ids).delete()
                if method == 1:
                    next_page = '/checkout/payment/' + str(header.id)
                elif method == 0:
                    next_page = '/checkout/result?id='+str(header.id)
                else:
                    raise Exception('Lỗi!')
                return Response({'message': 'Đặt hàng thành công', 'order_id': header.id, 'next_page': next_page}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrderCancelView(APIView):
    authentication_classes = [CookieAuthenticateJWT]
    permission_classes = [IsAuthenticated]
    def roll_back_quantity(self, order_id):
        try:
            order = OrderHeaders.objects.get(id=order_id)
            details = OrderDetails.objects.filter(header=order)
            for detail in details:
                product = Products.objects.select_for_update().get(id=detail.product.id)
                product.quantity = F('quantity') + detail.quantity
                product.save()
            return True
        except Exception as e:
            return e

    def post(self, request):
        try:
            with transaction.atomic():
                if not request.user.is_authenticated:
                    raise Exception('Vui lòng đăng nhập để sử dụng')
                order_id = request.data.get('order_id', None)
                if order_id is None:
                    raise Exception('Không tồn tại đơn hàng')
                user = request.user.profile
                if request.user.is_superuser:
                    order = OrderHeaders.objects.get(id=order_id)
                    order.order_status= -1 #Đã hủy
                    order.save()
                    print(self.roll_back_quantity(order_id))
                    return Response({'message': 'Hủy đơn hàng thành công'}, status.HTTP_202_ACCEPTED)
                else:
                    order = OrderHeaders.objects.get(user=user, id=order_id)
                if order is None:
                    raise Exception('Không tìm thấy đơn hàng')
                elif order.order_status == -1:
                    raise Exception('Đơn hàng đã hủy!')
                elif order.order_status >= 2:
                    order.order_status = -2 #Đợi admin xác nhận
                    order.save()
                elif order.order_status in [0,1]:
                    order.order_status = -1 #đã hủy
                    order.save()
                    print(self.roll_back_quantity(order_id))
                    return Response({'message': 'Hủy đơn hàng thành công!'}, status.HTTP_202_ACCEPTED)
                else:
                    raise Exception('Something went wrong!')
        except Exception as e:
            return Response({'message': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
class OrderPreviewList(APIView):
    authentication_classes = [CookieAuthenticateJWT]
    def check_quantity(self, quantity, product):
        if product.quantity == 0:
            raise Exception('Sản phẩm đã hết hàng!')
        return quantity <= product.quantity
    #Tạo order
    def post(self, request):
        try:
            mode = request.data['mode']
            list_ids = request.data['list_ids']
            if mode == "buyNow":
                preview = Products.objects.filter(id__in=list_ids)
                quantity = int(request.data['quantity'])
                if quantity <= 0:
                    raise Exception('Số lượng sản phẩm phải lớn hon 0!')
                print(quantity)
                if self.check_quantity(quantity, preview.first()):
                    preview = ProductsSerializer(preview, many=True).data
                    result = []
                    for pro in preview:
                        result.append({'product': pro, 'quantity': quantity, 'sub_total': pro['unit_price']*quantity})
                    return Response(result, status=status.HTTP_200_OK)
                else:
                    raise Exception('Không đủ sản phẩm!')
            elif mode == 'order':
                header = CartHeaders.objects.get(account = request.user)
                preview = CartDetails.objects.filter(header = header).order_by('-id')
                preview = preview.filter(id__in=list_ids)
                result = []
                for pre in preview:
                    if self.check_quantity(pre.quantity, pre.product):
                        result.append(pre)
                    else:
                        raise Exception("Không đủ sản phẩm!")
                    if int(pre.quantity) <= 0:
                        raise Exception("Số lượng phải lớn hơn 0!")
                result = CartDetailsSerializer(result, many=True).data
                return Response(result, status=status.HTTP_200_OK)
            elif mode == 'reOrder':
                preview = OrderDetails.objects.filter(id__in=list_ids)
                result = []
                for pre in preview:
                    if self.check_quantity(pre.quantity, pre.product):
                        result.append(pre)
                    elif pre.quantity == 0:
                        raise Exception("Số lượng phải lớn hơn 0!")
                    else:
                        raise Exception("Không đủ sản phẩm!")
                result = OrderDetailsSerializer(result, many=True).data
                return Response(result, status=status.HTTP_200_OK)
            else:
                raise Exception('Lỗi!')
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminOrders(APIView):
    authentication_classes = [CookieAuthenticateJWT]
    permission_classes = [IsAdminUser]
    def get(self, request):
        try:
            if not request.user.is_superuser:
                raise AuthenticationError("Bạn không có quyền sử dụng chức năng này!")
            order_status = request.query_params.get('status', None)
            if(order_status != "null"):
                orders = OrderHeaders.objects.filter(order_status = order_status).order_by('-date')
            else:
                orders = OrderHeaders.objects.all().order_by('-date')
            serializer = OrdersSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        try:
            if not request.user.is_authenticated:
                raise AuthenticationError('Vui lòng đăng nhập!')
            month = request.data.get('month',None)
            year = request.data.get('year', timezone.now().year)
            orders = OrderHeaders.objects.filter(date__year=int(year)).order_by('date')
            if month:
                orders = orders.filter(date__month=int(month)).order_by('date')
            orders = OrdersSerializer(orders, many=True).data
            total = 0
            product_count = 0
            order_status = []
            for order in orders:
                order_status.append(order['order_status'])
                if order['order_status'] ==-1 or order['order_status'] == -2:
                    print('hủy r')
                    continue
                total += order['total']
                product_count += order['product_count']
            result = {}
            result['total'] = total
            result['product_sale_count'] = for_bar_chart_1(orders)
            result['order_count'] = len(orders)
            result['product_count'] = product_count
            result['order_status'] = for_pie_chart(order_status)
            result['pay_method'] = for_line_chart(orders)
            return Response(result , status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            if not request.user.is_superuser:
                raise PermissionError("Bạn không có quyền sử dụng chức năng này")
            order_id = request.data.get('order_id', None)
            if order_id:
                validator = ValidOrderHeader(request.data)
                valid_data = validator.valid_data()
                if validator.action and validator.action == "Cancel":
                    return OrderCancelView().post(request)
                with transaction.atomic():
                    orders = OrderHeaders.objects.select_for_update().filter(id=order_id)
                    order = orders.first()
                    if order:
                        for key,value in valid_data.items():
                            setattr(order, key, value)
                        order.save()
                        return Response({'message': "Cập nhật thành công"}, status=status.HTTP_200_OK)
                    raise FileNotFoundError("Đơn hàng không tồn tại")
            else:
                raise ValidationError("Dữ liệu không hợp lệ")
        except PermissionError as e:
                return Response({'message': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except FileNotFoundError as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)



