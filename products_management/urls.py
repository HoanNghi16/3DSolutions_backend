
from django.urls import path
from .views import getProducts, getDetails, getMaterials

urlpatterns = [
    path('show_products/', getProducts.as_view(), name='show_products'),
    path('show_details/', getDetails.as_view(), name='show_details'),
    path('show_materials/', getMaterials.as_view(), name='show_materials'),
]