from django.utils import timezone

from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput, TimeInput

from movie_shows.exceptions import InsufficientBalanceException, MovieShowsCollideException, InvalidDateSetException, \
    InvalidTimeRangException, InvalidDateRangeException
from movie_shows.models import CinemaHall, MovieShow, Order


class CinemaHallCreateForm(forms.ModelForm):
    class Meta:
        model = CinemaHall
        fields = '__all__'


class MovieShowCreateForm(forms.ModelForm):
    class Meta:
        model = MovieShow
        fields = ['movie', 'movie_hall', 'start_time', 'start_date', 'end_time', 'end_date', 'ticket_price']

        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'start_time': TimeInput(attrs={'type': 'time'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            'end_time': TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hall = cleaned_data.get('movie_hall')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_date >= end_date:
            self.add_error('start_date', 'Start date cannot be before end date.')

        if start_time >= end_time:
            self.add_error('start_time', 'Start time cannot be before end time.')

        if end_date < timezone.now().date():
            self.add_error('end_date', 'You cannot arrange movie shows for the past.')

        if hall and start_date and end_date and start_time and end_time:

            previous_shows = MovieShow.objects.filter(movie_hall=hall)
            if self.instance and self.instance.pk:
                previous_shows = previous_shows.exclude(pk=self.instance.pk)
            for show in previous_shows:
                if show.end_date > start_date:
                    if show.end_time > start_time:
                        self.add_error(None, 'This show collide with another show.')


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['seat_quantity']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.customer = kwargs.pop('customer', None)
        self.movie_show = kwargs.pop('movie_show', None)
        super().__init__(*args, **kwargs)

    def clean_seat_quantity(self):
        seat_quantity = self.cleaned_data.get('seat_quantity')
        available_seats = self.movie_show.movie_hall.seats - self.movie_show.sold_seats

        if seat_quantity < 1:
            raise ValidationError('Please choose at least one seat.')

        if seat_quantity > self.movie_show.movie_hall.seats:
            raise ValidationError('You specified more seats than available in the movie hall.')

        if seat_quantity > available_seats:
            raise forms.ValidationError('You specified more seats than available for this movie show.')

        if self.customer.balance < seat_quantity * self.movie_show.ticket_price:
            raise InsufficientBalanceException(
                'Sorry, it seems you do not have enough funds to complete this transaction.')

        return seat_quantity
