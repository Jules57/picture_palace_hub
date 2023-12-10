from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput, TimeInput

from movie_shows.models import CinemaHall, MovieShow


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
        start_time = cleaned_data.get('start_time')
        end_date = cleaned_data.get('end_date')
        end_time = cleaned_data.get('end_time')

        overlapping_shows = MovieShow.objects.filter(
                movie_hall=hall,
                start_date__lte=end_date,
                end_date__gte=start_date,
                start_time__lte=end_time,
                end_time__gte=start_time
        )

        if self.instance and self.instance.pk:
            overlapping_shows = overlapping_shows.exclude(pk=self.instance.pk)

        if overlapping_shows.exists():
            raise ValidationError("It seems another show is running at this time.")

        return cleaned_data
