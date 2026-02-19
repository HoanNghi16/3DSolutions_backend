from django.urls import path
from .views import OrdersView, OrderPreviewList, OrderCreateView

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='orders'),
    path('preview/', OrderPreviewList.as_view(), name='preview'),
    path('ordercreate/', OrderCreateView.as_view(), name='buynow'),
]