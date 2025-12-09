from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializer import UsersSerializer
from auth_user.models import UserAccounts
from django.contrib.auth import authenticate

class RegistraionView(APIView):

    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(erros = serializer._error, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.create()
            return Response(data = 'Success', status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data = 'Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

class LoginView(APIView):
    def post(self, request):
        data = request.data
        user_authenticated = authenticate(request, email=data['email'], password=data['password'])
        if not user_authenticated:
            return Response(data = 'Invalid credentials', status=status.HTTP_401_UNAUTHORIZED)
        try:
            token_data = get_token_for_user(user_authenticated)
            return Response( token_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data = 'Token Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)