from carts_management.models import CartDetails, CartHeaders
from rest_framework import serializers

from products_management.serializer import ProductsSerializer


class CardDetailsSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)
    class Meta:
        model = CartDetails
        fields = ['id','product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    cart_details = CardDetailsSerializer(many=True, read_only=True)
    class Meta:
        model = CartHeaders
        fields = ['cart_details']