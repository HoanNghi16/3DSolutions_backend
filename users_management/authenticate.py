from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from .models import Users, UserAccounts
from rest_framework.exceptions import AuthenticationFailed

class CookieAuthenticateJWT(BaseAuthentication):
    def authenticate(self, request):
        access = request.COOKIES.get('access')
        print("COOKIES:", request.COOKIES)
        if not access:
            return None
        try:
            token = AccessToken(access)
            id = token['id']
            Account = UserAccounts.objects.get(id = id)
        except Exception:
            raise AuthenticationFailed('Fail')
        return (Account, token)



