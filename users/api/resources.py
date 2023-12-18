from django.contrib.auth.hashers import make_password
from rest_framework import views, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from users.api.permissions import IsProfileOwner
from users.api.serializers import CustomerSerializer, CustomerRegisterSerializer
from users.models import Customer, BearerTokenAuthentication


class AuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'pk': user.pk,
            'token': token.key,
        })


class LogoutApiView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    authentication_classes = [BearerTokenAuthentication]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomerRegisterSerializer
        return CustomerSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = []
        elif self.action in ['list']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsProfileOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        password = make_password(serializer.validated_data['password'])
        user = serializer.save(password=password)
        Token.objects.get_or_create(user=user)
