from rest_framework import status
from rest_framework.response import Response

from movie_shows.models import MovieShow, CinemaHall


class CheckSoldSeatsMixin(object):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if isinstance(instance, MovieShow):
            if instance.sold_seats > 0:
                return Response({"detail": "Cannot delete movie show with sold tickets."},
                                status=status.HTTP_400_BAD_REQUEST)

        elif isinstance(instance, CinemaHall):
            booked_shows = MovieShow.objects.filter(movie_hall=instance, sold_seats__gt=0)
            if booked_shows.exists():
                return Response({'detail': 'Cannot delete a movie hall with booked movie shows.'},
                                status=status.HTTP_400_BAD_REQUEST)

        return super().destroy(request, *args, **kwargs)
