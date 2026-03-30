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

class OrdersListSerializer(serializers.ModelSerializer):
    list_ids = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    class Meta:
        model = OrderHeaders
        fields = '__all__'
    def get_list_ids(self, obj):
        order_details = OrderDetails.objects.filter(header = obj)
        result = []
        for detail in order_details:
            result.append(detail.id)
        return result
    def get_date(self,obj):
        date = obj.date
        return date.strftime("%d/%m/%Y")

class OrdersSerializer(serializers.ModelSerializer):
    details = OrderDetailsSerializer(many=True, read_only=True)
    list_ids = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()
    class Meta:
        model = OrderHeaders
        fields = '__all__'
    def get_date(self,obj):
        date = obj.date
        return date.strftime("%d/%m/%Y")

    def get_list_ids(self, obj):
        order_details = OrderDetails.objects.filter(header=obj)
        result = []
        for detail in order_details:
            result.append(detail.id)
        return result
    def get_product_count(self, obj):
        order_details = OrderDetails.objects.filter(header=obj)
        result = 0
        for detail in order_details:
            result += detail.quantity
        return result

class AdminSummarySerializer(serializers.ModelSerializer):
    class Meta:
        mmodel = OrderHeaders
        fields = ['total']


class ValidOrderHeader:
    def __init__(self, data):
        self.receiver_name = data['receiver_name']
        self.receiver_phone = data['receiver_phone']