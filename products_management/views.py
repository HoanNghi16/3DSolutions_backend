from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Products, ProductImages, Materials
from rest_framework import status, request


# Create your views here.
class getProducts(APIView):
    def get(self, request):
        try:
            products_list = Products.objects.all()
            if len(products_list) == 0:
                return Response(data = str(None), status = status.HTTP_200_OK)
            product_images = {}
            for product in products_list:
                product_images[product.id] = ProductImages.objects.filter(id=product.id)[0].path
            return Response(data = f'products: {products_list}, images: {product_images}', status = status.HTTP_200_OK)
        except Exception as e:
            return Response(data = f'error: {e}', status = status.HTTP_500_INTERNAL_SERVER_ERROR)
class getDetails(APIView):
    def get(self, request):
        product_id = request.GET.get('id')
        product = Products.objects.get(id=product_id)
        images = ProductImages.objects.filter(product=product)
        return Response(data = f'product: {product}, images: {images}', status = status.HTTP_200_OK)
class getMaterials(APIView):
    def get(self, request):
        product_id = request.GET.get('id')
        if not product_id:
            materials_list = Materials.objects.all()
            return Response(data = f'materials: {materials_list}', status = status.HTTP_200_OK)
        try:
            material = Materials.objects.get(id=product_id)
            return Response(data = f'material: {material}', status = status.HTTP_200_OK)
        except Exception as e:
            return Response(data = f'error: {e}', status = status.HTTP_500_INTERNAL_SERVER_ERROR)