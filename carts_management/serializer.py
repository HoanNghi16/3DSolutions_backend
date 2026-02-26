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
    cart_details = serializers.SerializerMethodField()
    class Meta:
        model = CartHeaders
        fields = ['cart_details']
    def get_cart_details(self, obj):
        cart_details = CartDetails.objects.filter(header = obj).order_by('-date')
        print(cart_details)
        return CartDetailsSerializer(cart_details, many=True).data