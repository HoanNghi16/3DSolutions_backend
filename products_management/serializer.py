from rest_framework import serializers
from .models import Products, ProductImages, Materials

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['fileID', 'path', 'is_thumbnail']

class ProductsSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    class Meta:
        model = Products
        fields = ["id", "name", "unit_price", "quantity", "thumbnail"]

    def get_thumbnail(self, obj):
        thumbnail = obj.images.filter(is_thumbnail=True).first()
        if thumbnail:
            return thumbnail.path
        return None



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

