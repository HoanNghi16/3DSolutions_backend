from django.urls import path
from .views import OrdersView
urlpatterns = [
    path('orders/', OrdersView.as_view(), name='orders'),
]