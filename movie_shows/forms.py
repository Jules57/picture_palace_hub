from django.db.models import Q
from django.utils import timezone

from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.forms import DateInput, TimeInput

from movie_shows import exceptions
from movie_shows.models import CinemaHall, MovieShow, Order
from users.models import Customer


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
                        raise ValidationError


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['seat_quantity']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.customer = kwargs.pop('customer', None)
        self.movie_show_pk = kwargs.pop('movie_show_pk', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        try:
            movie_show = MovieShow.objects.get(pk=self.movie_show_pk)
            seat_quantity = cleaned_data.get('seat_quantity')
            available_seats = movie_show.movie_hall.seats - movie_show.sold_seats

            if seat_quantity < 1:
                self.add_error('seat_quantity',
                               'Zero seats.')
                messages.error(self.request,
                               'Please choose at least one seat.')

            if movie_show and seat_quantity:
                if seat_quantity > movie_show.movie_hall.seats:
                    self.add_error('seat_quantity',
                                   'Seats exceeded.')
                    messages.error(self.request,
                                   'You specified more seats than available in the movie hall.')

                elif seat_quantity > available_seats:
                    self.add_error('seat_quantity',
                                   'Seats unavailable.')
                    messages.error(self.request,
                                   'You specified more seats than available for this movie show.')

                if self.customer.balance < seat_quantity * movie_show.ticket_price:
                    self.add_error(None,
                                   'Insufficient balance.')
                    messages.error(self.request,
                                   'Sorry, it seems you do not have enough funds to complete this transaction.')

        except MovieShow.DoesNotExist:
            self.add_error(None, 'Error')
            messages.error(self.request,
                           'Movie show does not exist.')
