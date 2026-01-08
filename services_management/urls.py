from django.urls import path
from .views import ServiceOrdersView
urlpatterns = [
    path('orderservices/<uuid:id>', ServiceOrdersView.as_view(), name='service-orders'),
]