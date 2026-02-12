from django.urls import path
from .views import ServiceOrdersView, ServicesView

urlpatterns = [
    path('orderservices/<uuid:id>', ServiceOrdersView.as_view(), name='service-orders'),
    path('services/', ServicesView.as_view(), name='services'),
]