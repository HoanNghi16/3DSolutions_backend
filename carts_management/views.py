from rest_framework.status import HTTP_200_OK

from products_management.models import Products
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F
from carts_management.serializer import CartSerializer
from carts_management.models import CartHeaders, CartDetails
from users_management.authenticate import CookieAuthenticateJWT

class CartView(RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieAuthenticateJWT]
    def get_object(self):
        user = self.request.user
        cart = CartHeaders.objects.get(account = user)
        return cart

class CartChangeView(APIView):
    authentication_classes = [CookieAuthenticateJWT]
    #ADD TO CART
    def post(self, request):
        try:
            if not request.user.is_authenticated:
                raise Exception('Vui lòng đăng nhập để sử dụng giỏ hàng!')
            product_id = request.data['product']
            quantity = request.data['quantity']
            product = Products.objects.get(id=product_id)
            if product.quantity == 0:
                raise Exception('Sản phẩm đã hết hàng!')
            cart_header = CartHeaders.objects.get(account = request.user)

            cart_details = CartDetails.objects.filter(header = cart_header, product = product).first()
            if cart_details:
                cart_details = cart_details
                if product.quantity <= cart_details.quantity:
                    return Response(data= {"message": "Sản phẩm không đủ!"}, status=status.HTTP_400_BAD_REQUEST)
                cart_details.quantity = F('quantity') + quantity
                cart_details.save()
            else:
                CartDetails.objects.create(header = cart_header, product = product, quantity = quantity)

            cart_count = len(CartDetails.objects.filter(header = cart_header))
            return Response({'cart_count': cart_count, 'message': 'Đã thêm vào giỏ hàng'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

    #CHANGE QUANTITY
    def patch(self, request):
        user = request.user
        if (not user.is_authenticated):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            quantity = int(request.data['quantity'])
            product = Products.objects.get(id = request.data['product'])
            if quantity <= 0:
                raise Exception('Số lượng sản phẩm phải lớn hơn 0!')
            if(quantity > product.quantity):
                raise Exception('Sản phẩm không đủ!')
            detail_id = request.data['detail']
            cart_header = CartHeaders.objects.get(account = user)
            detail = CartDetails.objects.get(id = detail_id, header= cart_header)
            if not detail:
                raise Exception("Vui lòng thêm sản phẩm vào giỏ hàng!")
            detail.quantity = quantity
            detail.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if (not request.user.is_authenticated):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            cart_header = CartHeaders.objects.get(account = request.user)
            if not cart_header:
                raise Exception("Không tìm thấy giỏ hàng!")
            detail_id = request.data['detail']
            detail = CartDetails.objects.get(id = detail_id, header= cart_header)
            detail.delete()
            cart_count = len(CartDetails.objects.filter(header=cart_header))
            print(cart_count)
            return Response({'cart_count': cart_count, 'message': 'Đã xóa khỏi giỏ hàng!'},status=HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)},status=status.HTTP_400_BAD_REQUEST)