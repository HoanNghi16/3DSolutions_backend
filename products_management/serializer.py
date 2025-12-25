from rest_framework import serializers
from .models import Products, ProductImages, Materials

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['id', 'path']

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ["id", "name", "unit_price"]

class MaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materials
        fields = "__all__"

class ProductDetailsSerializer(serializers.ModelSerializer):
    images = ProductImagesSerializer(many=True, read_only=True)
    material = MaterialsSerializer(read_only=True)
    class Meta:
        model = Products
        fields = ['id', 'name', 'unit_price', 'quantity' , 'material', 'images']

