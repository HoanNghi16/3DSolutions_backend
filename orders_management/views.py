from django.shortcuts import render
from rest_framework.generics import ListAPIView

from orders_management.models import OrderHeaders


# Create your views here.

class OdersView(APIView):
