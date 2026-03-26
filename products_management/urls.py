
from django.urls import path
from .views import ProductsView, DetailsView, MaterialsView, CategoriesView, AdminProduct, AdminCateView

urlpatterns = [
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<uuid:id>/', DetailsView.as_view(), name='show_details'),
    path('materials/', MaterialsView.as_view(), name='show_materials'),
    path('categories/', CategoriesView.as_view(), name='show_categories'),
    path('admin_product/', AdminProduct.as_view(), name='admin_product'),
    path('admin_cate/', AdminCateView.as_view(), name='admin_cate'),
]