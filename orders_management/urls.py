from django.urls import path
from .views import OrdersView
urlpatterns = [
    path('orders/<uuid:user_id>/', OrdersView.as_view(), name='orders'),
]