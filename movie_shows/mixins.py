from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect

from movie_shows.models import MovieShow, CinemaHall


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class SoldTicketCheckMixin:
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if isinstance(self.object, MovieShow) and self.object.sold_seats > 0:
            messages.error(self.request, 'This movie show is already booked.')
            return HttpResponseRedirect(self.object.get_absolute_url())

        if isinstance(self.object, CinemaHall) and hasattr(self.object, 'shows') and any(
                show.sold_seats > 0 for show in self.object.shows.all()):
            messages.error(self.request, 'A movie show in this hall is already booked.')
            return HttpResponseRedirect(self.object.get_absolute_url())

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if isinstance(self.object, MovieShow) and self.object.sold_seats > 0:
            messages.error(self.request, 'This movie show is already booked.')
            return HttpResponseRedirect(self.object.get_absolute_url())

        if isinstance(self.object, CinemaHall) and hasattr(self.object, 'shows') and any(
                show.sold_seats > 0 for show in self.object.shows.all()):
            messages.error(self.request, 'A movie show in this hall is already booked.')
            return HttpResponseRedirect(self.object.get_absolute_url())

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        raise NotImplementedError
