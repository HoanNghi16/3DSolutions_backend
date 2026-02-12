
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from services_management.serializer import ServiceOrdersSerializer, ServiceOrderHeadersSerializer, ServicesSerializer
from services_management.models import ServiceOrderHeaders, Services


# Create your views here.
class ServicesView(ListAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer

class ServiceOrdersView(ListAPIView):
    serializer_class = ServiceOrdersSerializer
    def get_queryset(self):
        id = self.kwargs.get('id')
        return ServiceOrderHeaders.objects.filter(user=id)

class ServiceOrdersListView(ListAPIView):
    serializer_class = ServiceOrderHeadersSerializer
    def get_queryset(self):
        id = self.kwargs.get('id')
        return ServiceOrderHeaders.objects.filter(user=id)
