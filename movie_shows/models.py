from django.db import models
from django.urls import reverse

from users.models import Customer


class CinemaHall(models.Model):
    SCREEN_2D = '2D'
    SCREEN_3D = '3D'
    SCREEN_TYPE_CHOICES = [
        (SCREEN_2D, '2D Screen'),
        (SCREEN_3D, '3D Screen'),
    ]

    STANDARD = 'Standard'
    LARGE = 'Large'
    PREMIUM = 'Premium'
    SCREEN_SIZE_CHOICES = [
        (STANDARD, 'Standard'),
        (LARGE, 'Large'),
        (PREMIUM, 'Premium'),
    ]
    name = models.CharField(max_length=200)
    seats = models.PositiveIntegerField()
    screen_size = models.CharField(
            choices=SCREEN_SIZE_CHOICES,
            default=STANDARD,
            max_length=50,
    )
    screen_type = models.CharField(
            max_length=2,
            choices=SCREEN_TYPE_CHOICES,
            default=SCREEN_2D
    )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('shows:hall_detail', args=[self.id])


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration_in_minutes = models.PositiveIntegerField()
    director = models.CharField(max_length=128)
    poster = models.ImageField(
            upload_to='movie_images/',
            max_length=255,
            null=True,
            blank=True,
            default='static/img/movie_poster.jpg')

    def __str__(self):
        return f'{self.title}'


class MovieShow(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movies')
    movie_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='shows')
    start_time = models.TimeField()
    start_date = models.DateField()
    end_time = models.TimeField()
    end_date = models.DateField()
    sold_seats = models.PositiveIntegerField(default=0)
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'Show {self.id} at {self.start_time}'

    def get_absolute_url(self):
        return reverse('shows:show_detail', args=[self.id])


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    movie_show = models.ForeignKey(MovieShow, on_delete=models.CASCADE, related_name='orders')
    seat_quantity = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    ordered_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.customer.username}'
