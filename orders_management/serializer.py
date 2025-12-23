from orders_management.models import OrderHeaders, OrderDetails
from rest_framework import serializers

class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = "__all__"

class OrdersSerializer(serializers.ModelSerializer):
    details = OrderDetailsSerializer(many=True, read_only=True)
    class Meta:
        model = OrderHeaders
        fields = "__all__"