from django.db import models
from django.contrib.auth.models import AbstractUser

from movie_shows.models import MovieShow


class Customer(AbstractUser):
    image = models.ImageField(
            upload_to='user_images/',
            max_length=255,
            null=True,
            blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=10000000)


class CustomerProfile(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='profile')
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f'{self.customer.username}'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    movie_show = models.ForeignKey(MovieShow, on_delete=models.CASCADE, related_name='orders')
    seat_quantity = models.PositiveIntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    ordered_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.customer.username}'
