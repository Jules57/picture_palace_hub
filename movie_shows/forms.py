from django import forms
from django.forms import DateInput, TimeInput

from movie_shows.models import CinemaHall, MovieShow


class CinemaHallCreateForm(forms.ModelForm):
    class Meta:
        model = CinemaHall
        fields = '__all__'


class MovieShowCreateForm(forms.ModelForm):
    class Meta:
        model = MovieShow
        exclude = ['sold_seats']

    widgets = {
        'start_date': DateInput(attrs={'type': 'date'}),
        'start_time': TimeInput(attrs={'type': 'time'}),
        'end_date': DateInput(attrs={'type': 'date'}),
        'end_time': TimeInput(attrs={'type': 'time'}),
    }
