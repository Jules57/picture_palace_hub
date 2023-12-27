from django.contrib import messages
from django.utils import timezone

from django import forms
from django.forms import DateInput, TimeInput

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
        fields = ['seat_quantity', 'movie_show']
        widgets = {'movie_show': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.movie_show_id = kwargs.pop('movie_show_id', None)
        super().__init__(*args, **kwargs)

        self.fields['movie_show'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        seat_quantity = self.cleaned_data.get('seat_quantity')

        movie_show = self.cleaned_data.get('movie_show', None)
        if movie_show is None:
            movie_show = MovieShow.objects.get(pk=self.movie_show_id)
            self.add_error(None, 'Changed hidden field')
            messages.error(self.request,
                           'Don\'t mess up with this hidden field, Vlad.')

        if seat_quantity < 1:
            self.add_error('seat_quantity', 'Zero seats.')
            messages.error(self.request,
                           'Please choose at least one ticket.')

        if seat_quantity > movie_show.movie_hall.seats:
            self.add_error('seat_quantity', 'Too many seats selected.')
            messages.error(self.request,
                           'You specified more tickets than available in this movie hall.')

        if seat_quantity > movie_show.movie_hall.seats - movie_show.sold_seats:
            self.add_error('seat_quantity', 'Too many seats selected.')
            messages.error(self.request,
                           'You specified more seats than available for this movie show.')

        if self.request.user.balance < seat_quantity * movie_show.ticket_price:
            self.add_error(None, 'Insufficient balance.')
            messages.error(self.request,
                           'Sorry, it seems you do not have enough balance to complete this transaction.')

        return cleaned_data
