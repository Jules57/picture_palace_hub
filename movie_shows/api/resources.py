from datetime import timedelta

from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.datetime_safe import datetime
from rest_framework import viewsets, serializers, mixins
from rest_framework.permissions import IsAuthenticated

from movie_shows.api.mixins import CheckSoldSeatsMixin
from movie_shows.api.serializers import CinemaHallWriteSerializer, CinemaHallReadSerializer, MovieShowWriteSerializer, \
    MovieShowReadSerializer, MovieReadSerializer, OrderWriteSerializer
from movie_shows.models import CinemaHall, MovieShow, Movie, Order
from users.api.permissions import IsAdminOrReadOnly


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = MovieReadSerializer


class CinemaHallViewSet(CheckSoldSeatsMixin, viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return CinemaHallWriteSerializer
        return CinemaHallReadSerializer


class MovieShowViewSet(CheckSoldSeatsMixin, viewsets.ModelViewSet):
    queryset = MovieShow.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return MovieShowWriteSerializer
        return MovieShowReadSerializer

    def get_queryset(self):
        queryset = MovieShow.objects.all()
        if self.request.method == 'GET':
            if self.request.query_params.get('day') == 'today':
                today = timezone.now().date()
                queryset = queryset.filter(start_date__lte=today, end_date__gte=today).order_by('start_time')

                from_time = self.request.query_params.get('from', None)
                to_time = self.request.query_params.get('to', None)
                hall = self.request.query_params.get('hall', None)

                if from_time and to_time:
                    from_time = datetime.strptime(from_time, "%H:%M").time()
                    to_time = datetime.strptime(to_time, "%H:%M").time()
                    queryset = queryset.filter(
                            (Q(start_time__gte=from_time) & Q(start_time__lte=to_time))
                    ).order_by('start_time')

                if hall:
                    queryset = queryset.filter(movie_hall=hall).order_by('start_time')

            elif self.request.query_params.get('day') == 'next_day':
                next_day = timezone.now().date() + timedelta(days=1)
                queryset = queryset.filter(
                        start_date__lte=next_day,
                        end_date__gte=next_day
                )

            sort_by = self.request.query_params.get('sort_by')
            if sort_by == 'start_time':
                queryset = queryset.order_by('start_time')
            elif sort_by == '-start_time':
                queryset = queryset.order_by('-start_time')
            elif sort_by == 'price':
                queryset = queryset.order_by('ticket_price')
            elif sort_by == '-price':
                queryset = queryset.order_by('-ticket_price')

        return queryset


class OrderViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OrderWriteSerializer

    def perform_create(self, serializer):
        try:
            movie_show = serializer.validated_data['movie_show']
            seat_quantity = serializer.validated_data['seat_quantity']

            movie_show.sold_seats += seat_quantity
            total_cost = seat_quantity * movie_show.ticket_price
            customer = self.request.user
            customer.balance -= total_cost

            with transaction.atomic():
                serializer.save(customer=self.request.user, total_cost=total_cost)
                customer.save()
                movie_show.save()
        except Exception as e:
            raise serializers.ValidationError(str(e))
