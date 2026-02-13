from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from products_management.models import Products
from users_management.authenticate import CookieAuthenticateJWT
from .models import OrderHeaders, OrderDetails
from .serializer import OrdersSerializer
from users_management.models import Users


# Create your views here.
class OrdersView(ListAPIView):
    serializer_class = OrdersSerializer
    authentication_classes = [CookieAuthenticateJWT]
    def get_queryset(self):
        name = self.request.query_params.get('name', None)
        phone = self.request.query_params.get('phone', None)
        user = None
        if name and phone:
            user = Users.objects.get(name=name, phone=phone)
        if not user:
            user = self.request.user.profile
        order = OrderHeaders.objects.filter(user=user)
        return order

class BuyNowView(APIView):
    def post(self, request):
        profile = request.data['profile']
        product = request.data['product']
        quantity = request.data['quantity']
        pay_status = request.data['pay_status']
        method = request.data['method']
        status = request.data['status']

        if profile and product and quantity:
            profile  = Users.objects.get(name=profile)
            product = Products.objects.get(id=product)
            header = OrderHeaders.objects.create(user = profile, total = quantity*product.unit_price, pay_status = pay_status, method = method, status = status )
            detail = OrderDetails.objects.create(header = header, product = product, quantity = quantity)
            header.save()
            detail.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)



