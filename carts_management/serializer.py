from carts_management.models import CartDetails, CartHeaders
from rest_framework import serializers

from products_management.serializer import ProductsSerializer


class CartDetailsSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)
    sub_total = serializers.SerializerMethodField()
    class Meta:
        model = CartDetails
        fields = ['id','product', 'quantity', 'sub_total']
    def get_sub_total(self, obj):
        return obj.product.unit_price * obj.quantity
class CartSerializer(serializers.ModelSerializer):
    cart_details = CartDetailsSerializer(many=True, read_only=True)
    class Meta:
        model = CartHeaders
        fields = ['cart_details']