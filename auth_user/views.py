from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import UsersSerializer
from django.contrib.auth import authenticate
from .models import UserAccounts, Users

class RegistraionView(APIView):

    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data = serializer._error, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.create()
            return Response(data = f'serializer created', status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data = f'{e.args}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_token_for_user(user):
    print(user)
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

class LoginView(APIView):
    def post(self, request):
        data = request.data
        user_authenticated = authenticate(request,email=data.get('email'), password=data.get('password'))
        if not user_authenticated:
            return Response(data = 'Invalid credentials ' + f'{user_authenticated}', status=status.HTTP_401_UNAUTHORIZED)
        try:
            token_data = get_token_for_user(user_authenticated)
            return Response( token_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data = 'Token Error' + f'{e.args}' + f'{user_authenticated}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        return Response(data = f'{Users.objects.all()}) ' + f'{UserAccounts.objects.all()}', status=status.HTTP_200_OK)