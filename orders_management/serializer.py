from orders_management.models import OrderHeaders, OrderDetails
from rest_framework import serializers
from products_management.serializer import ProductsSerializer
from users_management.models import Users
from products_management.models import Products


class OrderDetailsSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)
    class Meta:
        model = OrderDetails
        fields = ['product', 'quantity']

class OrdersSerializer(serializers.ModelSerializer):
    details = OrderDetailsSerializer(many=True, read_only=True)
    class Meta:
        model = OrderHeaders
        fields = ['id', 'user_id', 'pay', 'method', 'details']
