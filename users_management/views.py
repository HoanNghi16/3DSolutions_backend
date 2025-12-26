from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .authenticate import CookieAuthenticateJWT
from .serializer import UsersSerializer, UserInformationsSerializer, UserAccountsSerializer
from django.contrib.auth import authenticate
from .models import UserAccounts, Users
from core import settings
from rest_framework.permissions import AllowAny

class RegistrationView(APIView):
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
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    authentication_classes = []  # 🔥 QUAN TRỌNG
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        user_authenticated = authenticate(request,email=data.get('email'), password=data.get('password'))
        if not user_authenticated:
            return Response(data = 'Invalid credentials ', status=status.HTTP_401_UNAUTHORIZED)
        try:
            user_get_token = UserAccounts.objects.get(email=data.get('email'))
            token_data = get_token_for_user(user_get_token)
            response = Response({'message': 'success'}, status = status.HTTP_200_OK)
            #Set cookies cho login
            response.set_cookie(key='access',
                                value=token_data['access'],
                                httponly=True,
                                secure = False,
                                samesite = 'Lax',
                                max_age = 60*15,
                                path='/') #15 mins

            response.set_cookie(key='refresh',
                                value=token_data['refresh'],
                                httponly=True,
                                secure = False,
                                samesite='Lax',
                                max_age= 60*60*24*7, #1 week
                                path='/')
            return response
        except Exception as e:
            return Response(data = 'Token Error' + f'{e.args}' + f'{user_authenticated}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserInformationView(RetrieveAPIView):
    serializer_class = UserAccountsSerializer
    authentication_classes = [CookieAuthenticateJWT]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user