import datetime

from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from picture_palace_hub import settings


class TokenExpiredAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if token.created < timezone.now() - datetime.timedelta(seconds=settings.TOKEN_TTL):
            token.delete()
            raise AuthenticationFailed(f'Token was created more the {settings.TOKEN_TTL} seconds ago.')

        return token.user, token
