from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authentication import TokenAuthentication


class Customer(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=10000000)


class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'
