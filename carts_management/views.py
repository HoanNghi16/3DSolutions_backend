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


# Create your views here.
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
    permission_classes = [IsAuthenticated]

    #ADD TO CART
    def post(self, request):
        try:
            product_id = request.data['product']
            quantity = request.data['quantity']
            print(product_id, quantity)
            cart_header = CartHeaders.objects.get(account = request.user)
            product = Products.objects.get(id = product_id)
            cart_details = CartDetails.objects.filter(header = cart_header, product = product).first()
            if cart_details:
                cart_details = cart_details
                if product.quantity <= cart_details.quantity:
                    return Response(data= '{"message": "Over in stock quantity"}', status=status.HTTP_400_BAD_REQUEST)
                cart_details.quantity = F('quantity') + quantity
                cart_details.save()
            else:
                CartDetails.objects.create(header = cart_header, product = product, quantity = quantity)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    #CHANGE QUANTITY
    def patch(self, request):
        if (not request.user.is_authenticated):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            quantity = request.data['quantity']
            detail_id = request.data['detail']
            cart_header = CartHeaders.objects.get(account = request.user)
            detail = CartDetails.objects.get(id = detail_id, header= cart_header)
            if not detail:
                raise Exception("Not found")
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
                raise Exception("Not found")
            detail_id = request.data['detail']
            detail = CartDetails.objects.get(id = detail_id, header= cart_header)
            detail.delete()
            return Response(status=HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)},status=status.HTTP_400_BAD_REQUEST)