from django.utils import timezone
from picture_palace_hub import settings
from rest_framework import exceptions

from users.models import BearerTokenAuthentication


class TokenExpiredAuthentication(BearerTokenAuthentication):
    def authenticate(self, request):
        try:
            user, token = super().authenticate(request=request)
        except TypeError:
            return None

        if (timezone.now() - token.created).seconds > settings.TOKEN_TTL:
            token.delete()
            raise exceptions.AuthenticationFailed(
                f'Token was created more the {settings.TOKEN_TTL} seconds ago.'
            )
        return user, token
