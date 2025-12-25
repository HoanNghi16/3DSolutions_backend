from django.utils.timezone import override
from rest_framework import status
from rest_framework.generics import ListAPIView
from .serializer import OrdersSerializer
from .models import OrderHeaders


# Create your views here.
class OrdersView(ListAPIView):
    serializer_class = OrdersSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return OrderHeaders.objects.filter(user_id=user_id)



