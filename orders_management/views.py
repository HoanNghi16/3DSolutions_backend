from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carts_management.models import CartHeaders, CartDetails
from products_management.models import Products
from products_management.serializer import ProductsSerializer
from users_management.authenticate import CookieAuthenticateJWT
from .models import OrderHeaders, OrderDetails
from .serializer import OrdersSerializer
from users_management.models import Users


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
            if request.user.is_authenticated:
                header = OrderHeaders.objects.create(user = request.user.profile,**request.data['header'])
            else:
                header = OrderHeaders.objects.create(**request.data['header'], user = None)
            if header:
                details = request.data['details']
                for detail in details:
                    product = Products.objects.get(id = detail['product']['id'])
                    term = OrderDetails.objects.create(header = header,product = product, quantity = detail['quantity'])
                    term.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': e},status=status.HTTP_400_BAD_REQUEST)


class OrderPreviewList(APIView):
    def check_quantity(self, quantity, product):
        return quantity <= product.quantity

    def post(self, request):
        mode = request.data['mode']
        list_ids = request.data['list_ids']
        quantity = int(request.data['quantity'])
        if mode == "buyNow":
            preview = Products.objects.filter(id__in=list_ids)
            if self.check_quantity(quantity, preview.first()):
                preview = ProductsSerializer(preview, many=True).data
                return Response(preview, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            header = CartHeaders.objects.get(account = request.user)
            preview = CartDetails.filter(header = header)
        list_ids = request.data['list_ids']
        if list_ids:
            preview = preview.filter(id__in=list_ids)
            preview = ProductsSerializer(preview, many=True).data
            return Response(data=preview, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)



