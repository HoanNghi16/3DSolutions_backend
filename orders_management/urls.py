from django.urls import path
from .views import OrdersView, OrderPreviewList, OrderCreateView, OrderCancelView, OrderDetailsView

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='orders'),
    path('preview/', OrderPreviewList.as_view(), name='preview'),
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('order_cancel/', OrderCancelView.as_view(), name='order_cancel'),
    path('orders/<uuid:id>/', OrderDetailsView.as_view(), name='order_details'),
]