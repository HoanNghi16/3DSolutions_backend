from rest_framework import serializers
from .models import Products, ProductImages, Materials, Categories


class CategoriesSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    class Meta:
        model = Categories
        fields = ['id', 'name', 'children', 'parent']
    def get_children(self, obj):
        children = obj.children.all()
        return CategoriesSerializer(children, many=True).data

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['fileID', 'path', 'is_thumbnail']

class ProductMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materials
        fields = ["name"]
class AdminCateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name']
class ProductsSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    material = ProductMaterialSerializer()
    category = AdminCateSerializer(read_only=True)
    class Meta:
        model = Products
        fields = ["id", "name", "unit_price", "quantity", "thumbnail", "material", "category"]

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
        fields = ['id', 'name', 'unit_price', 'quantity' , 'material', 'images', 'rate', 'description']

