
from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from .models import UserAccounts
from rest_framework.exceptions import AuthenticationFailed

class CookieAuthenticateJWT(BaseAuthentication):
    def authenticate(self, request):
        access = request.headers.get('Authorization')
        if not access:
            return None
        try:
            token = AccessToken(access)
            id = token['id']
            Account = UserAccounts.objects.get(id = id)
        except Exception:
            raise AuthenticationFailed('Fail')
        return (Account, token)



