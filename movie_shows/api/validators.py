from django.utils import timezone
from rest_framework import serializers

from movie_shows.models import MovieShow


def validate_date_range(start_date, end_date):
    if start_date and end_date and start_date > end_date:
        raise serializers.ValidationError('Start date cannot be before end date')


def validate_time_range(start_time, end_time):
    if start_time and end_time and start_time >= end_time:
        raise serializers.ValidationError('Start time cannot be before end time.')


def validate_past_date(end_date):
    if end_date and end_date < timezone.now().date():
        raise serializers.ValidationError('You cannot arrange movie shows for the past')


def validate_collisions(self, movie_hall, start_date, end_date, start_time, end_time):
    if all([movie_hall, start_date, end_date, end_time]):
        previous_shows = MovieShow.objects.filter(movie_hall=movie_hall)
        if self.instance:
            previous_shows = previous_shows.exclude(pk=self.instance.pk)
        for show in previous_shows:
            if show.end_date > start_date and show.end_time > start_time:
                raise serializers.ValidationError('This show collides with another show in this hall.')


def validate_available_seats(movie_show, seat_quantity):
    if movie_show and seat_quantity:
        available_seats = movie_show.movie_hall.seats - movie_show.sold_seats
        if seat_quantity > available_seats:
            raise serializers.ValidationError('You specified more seats than available for this movie show.')

        if seat_quantity > movie_show.movie_hall.seats:
            raise serializers.ValidationError('You specified more seats than available in the movie hall.')


def check_balance(movie_show, seat_quantity, customer):
    if customer.balance < seat_quantity * movie_show.ticket_price:
        raise serializers.ValidationError('Sorry, it seems you do not have enough funds to complete this transaction.')
