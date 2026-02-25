from django.urls import path

from carts_management.views import CartView, CartChangeView

urlpatterns = [
    path('cart/', CartView.as_view(), name='get_cart'),
    path('cart_change/', CartChangeView.as_view(), name='add_to_cart'),
]