
from django.urls import path
from .views import ProductsView, DetailsView, MaterialsView

urlpatterns = [
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<uuid:id>/', DetailsView.as_view(), name='show_details'),
    path('materials/', MaterialsView.as_view(), name='show_materials'),
]