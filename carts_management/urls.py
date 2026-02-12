from django.urls import path

from carts_management.views import CartView, AddToCartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='get_cart'),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
]