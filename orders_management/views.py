from datetime import timezone, timedelta

from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F

from carts_management.models import CartHeaders, CartDetails
from carts_management.serializer import CartDetailsSerializer
from products_management.models import Products
from products_management.serializer import ProductsSerializer
from users_management.authenticate import CookieAuthenticateJWT
from users_management.models import Address
from .models import OrderHeaders, OrderDetails
from .serializer import OrdersSerializer


# Create your views here.
class OrdersView(ListAPIView):
    serializer_class = OrdersSerializer
    authentication_classes = [CookieAuthenticateJWT]
    def get_queryset(self):
        user = self.request.user.profile
        order = OrderHeaders.objects.filter(user=user)
        print(order)
        return order

class OrderCreateView(APIView):
    authentication_classes = [CookieAuthenticateJWT]
    def post(self, request):
        try:
            with transaction.atomic():
                #order_status: 0 -> ordered, 1 -> confirmed, 2-> Packed, 3 -> On delivery, 4 -> finish
                #pay_method: 0 = cash, 1 = online
                #pay_status: 0 = unpaid, 1 = paid, -1 = wait (only for online payment)
                #Frontend will send pay_method only, all default value is 0

                details = request.data.get('details', None)
                if not details:
                    raise Exception('Order must has at least one product')
                user = request.user.profile if request.user.is_authenticated else None
                method = request.data.get('method', 0)
                if method == 1:
                    pay_status = -1
                    expire_at = timezone.now() + timedelta(hours=1)
                else:
                    pay_status = 0
                    expire_at = None
                total = 0
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
                                                     city=city, ward=ward, total = total, expire_at = expire_at)
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
                list_ids = request.data.get('list_ids', None)
                if list_ids and user:
                    header = CartHeaders.objects.get(account = request.user if request.user.is_authenticated else None)
                    if header:
                        CartDetails.objects.filter( id__in = list_ids).delete()
                header.total = total
                header.save()
                return Response({'message': 'success'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrderPreviewList(APIView):
    authentication_classes = [CookieAuthenticateJWT]
    def check_quantity(self, quantity, product):
        return quantity <= product.quantity
    def post(self, request):
        mode = request.data['mode']
        list_ids = request.data['list_ids']
        if mode == "buyNow":
            preview = Products.objects.filter(id__in=list_ids)
            quantity = int(request.data['quantity'] if request.data['quantity'] else 1)
            if self.check_quantity(quantity, preview.first()):
                preview = ProductsSerializer(preview, many=True).data
                result = []
                for pro in preview:
                    result.append({'product': pro, 'quantity': quantity, 'sub_total': pro['unit_price']*quantity})
                return Response(result, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif mode == 'order':
            print(request.user)
            header = CartHeaders.objects.get(account = request.user)
            preview = CartDetails.objects.filter(header = header)
            preview = preview.filter(id__in=list_ids)
            result = []
            for pre in preview:
                if self.check_quantity(pre.quantity, pre.product):
                    result.append(pre)
            result = CartDetailsSerializer(result, many=True).data
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



