from django.urls import path
from .views import OrdersView, OrderPreviewList, BuyNowView

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='orders'),
    path('preview/', OrderPreviewList.as_view(), name='preview'),
    path('buynow/', BuyNowView.as_view(), name='buynow'),
]