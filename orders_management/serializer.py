from orders_management.models import OrderHeaders, OrderDetails
from rest_framework import serializers
from products_management.serializer import ProductsSerializer


class OrderDetailsSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)
    sub_total = serializers.SerializerMethodField()
    class Meta:
        model = OrderDetails
        fields = ['product', 'quantity', 'sub_total', 'current_price']
    def get_sub_total(self, obj):
        return obj.current_price*obj.quantity

class OrdersSerializer(serializers.ModelSerializer):
    details = OrderDetailsSerializer(many=True, read_only=True)
    class Meta:
        model = OrderHeaders
        fields = '__all__'
