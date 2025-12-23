from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users_management.models import Users
from .serializer import OrderList


# Create your views here.
class OrdersView(APIView):
    def get(self, request, user_id):
        try:
            user = Users.objects.get(user_id = user_id)
            serializer = OrderList(user)
            result = serializer.result()
            if result is None:
                return Response( data= 0 ,status=status.HTTP_200_OK)
            else:
                return Response(data = result, status = status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status = status.HTTP_400_BAD_REQUEST)

