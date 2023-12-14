from django.db import models
from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    image = models.ImageField(
            upload_to='user_images/',
            max_length=255,
            null=True,
            blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=10000000)
