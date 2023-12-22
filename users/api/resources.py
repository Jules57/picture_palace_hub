from django.contrib.auth.hashers import make_password
from rest_framework import views, status, viewsets
from rest_framework.authtoken.models import Token

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from users.api.permissions import IsProfileOwner
from users.api.serializers import CustomerWriteSerializer, CustomerRegisterSerializer, CustomerReadSerializer
from users.models import Customer, BearerTokenAuthentication


class LogoutApiView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(id__in=[self.request.user.pk])
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomerRegisterSerializer
        elif self.request.method == 'GET' and self.request.query_params.get('profile', '') == 'my':
            return CustomerReadSerializer
        return CustomerReadSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = []
        elif self.action in ['list']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        password = make_password(serializer.validated_data['password'])
        user = serializer.save(password=password)
        Token.objects.get_or_create(user=user)
