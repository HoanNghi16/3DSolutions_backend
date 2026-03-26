from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from carts_management.models import CartHeaders
from .authenticate import CookieAuthenticateJWT
from .serializer import UsersSerializer, UserAccountsSerializer, AccountsAdminSerializer
from django.contrib.auth import authenticate
from .models import UserAccounts, Address

class RegistrationView(APIView):
    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer._error)
            return Response(serializer._error, status=status.HTTP_409_CONFLICT)
        try:
            new_account = serializer.create()
            print(new_account)
            if new_account:
                new_cart = CartHeaders.objects.create(account = new_account)
                new_cart.save()
                print(new_cart)
            return Response(data = f'account created', status=status.HTTP_201_CREATED)
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
    def post(self, request):
        print(request.data)
        data = request.data
        user_authenticated = authenticate(request,email=data.get('email'), password=data.get('password'))
        print(user_authenticated)
        if not user_authenticated:
            return Response(data = 'Invalid credentials ', status=status.HTTP_401_UNAUTHORIZED)
        try:
            user_get_token = UserAccounts.objects.get(email=data.get('email'))
            token_data = get_token_for_user(user_get_token)
            response = Response({'access': token_data['access'], 'refresh': token_data['refresh']}, status = status.HTTP_200_OK)
            return response
        except Exception as e:
            return Response(data = 'Token Error' + f'{e.args}' + f'{user_authenticated}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserInformationView(RetrieveAPIView):
    serializer_class = UserAccountsSerializer
    authentication_classes = [CookieAuthenticateJWT]
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh = request.headers.get('refresh')
            token = RefreshToken(refresh)
            #add token to blacklist (delete refresh token)
            token.blacklist()
            response = Response({'message': 'success'}, status=status.HTTP_200_OK)
            response.delete_cookie(key = 'access')
            response.delete_cookie(key = 'refresh')
            return response
        except Exception as e:
            return Response(data = f'{e.args}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NewAddressView(APIView):
    authentication_classes = [CookieAuthenticateJWT]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            if request.data:
                if '' in request.data.values() or None in request.data.values():
                    return Response(data = {'message': "No data sent"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(data = {'message': "No data sent"}, status=status.HTTP_404_NOT_FOUND)
            if request.user.is_authenticated:
                address = Address.objects.create( user = request.user.profile,**(request.data))
                address.save()
                return Response({'message': 'success'}, status=status.HTTP_201_CREATED)
            else:
                return Response(data = {'message': "Please log in"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response(data=f'{e}',status = status.HTTP_500_INTERNAL_SERVER_ERROR)

class UsersAdminView(APIView):
    authentication_classes = [CookieAuthenticateJWT]
    permission_classes = [IsAdminUser]
    def get(self, request):
        try:
            users = UserAccounts.objects.all()
            serializer = AccountsAdminSerializer(users, many=True)
            return Response(data = serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data = f'{e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
