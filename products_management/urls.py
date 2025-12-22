
from django.urls import path
from .views import getProducts, getDetails, getMaterials

urlpatterns = [
    path('products/', getProducts.as_view(), name='products'),
    path('products/<uuid:id>/', getDetails.as_view(), name='show_details'),
    path('materials/', getMaterials.as_view(), name='show_materials'),
]