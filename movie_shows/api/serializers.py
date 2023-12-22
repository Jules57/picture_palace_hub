from rest_framework import serializers

from movie_shows.api.validators import validate_collisions, validate_past_date, validate_time_range, \
    validate_date_range, check_balance, validate_available_seats
from movie_shows.models import CinemaHall, MovieShow, Movie, Order


class MovieReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'duration_in_minutes', 'director']


class MovieShowReadSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField(read_only=True)
    movie_hall = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MovieShow
        fields = ['id', 'movie', 'movie_hall', 'start_time', 'start_date', 'end_time', 'end_date', 'sold_seats',
                  'ticket_price']


class MovieShowWriteSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    movie_hall = serializers.PrimaryKeyRelatedField(queryset=CinemaHall.objects.all())

    class Meta:
        model = MovieShow
        fields = ['id', 'movie', 'movie_hall', 'start_time', 'start_date',
                  'end_time', 'end_date', 'sold_seats', 'ticket_price']

    def validate(self, data):
        start_date = data.get('start_date', self.instance.start_date if self.instance else None)
        end_date = data.get('end_date', self.instance.end_date if self.instance else None)
        start_time = data.get('start_time', self.instance.start_time if self.instance else None)
        end_time = data.get('end_time', self.instance.end_time if self.instance else None)
        movie_hall = data.get('movie_hall', self.instance.movie_hall if self.instance else None)

        validate_date_range(start_date, end_date)
        validate_time_range(start_time, end_time)
        validate_past_date(end_date)

        if self.instance:
            if self.instance.sold_seats > 0:
                raise serializers.ValidationError('You cannot delete or update a movie show with sold seats.')
            validate_collisions(self, movie_hall, start_date, end_date, start_time, end_time)
        return data


class CinemaHallReadSerializer(serializers.ModelSerializer):
    shows = MovieShowReadSerializer(many=True, read_only=True)

    class Meta:
        model = CinemaHall
        fields = ['id', 'name', 'seats', 'screen_size', 'screen_type', 'shows']


class CinemaHallWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = ['id', 'name', 'seats', 'screen_size', 'screen_type']

    def validate(self, data):
        if any([show.sold_seats > 0 for show in self.instance.shows.all()]):
            raise serializers.ValidationError('You cannot modify a cinema hall with booked shows.')
        return data


class OrderReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'movie_show', 'seat_quantity', 'total_cost', 'ordered_at']
        read_only_fields = ['customer']


class OrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'movie_show', 'seat_quantity', 'total_cost', 'ordered_at']
        read_only_fields = ['customer']

    def validate_seat_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError('Please choose at least one seat.')
        return value

    def validate(self, data):
        movie_show = data['movie_show']
        seat_quantity = data['seat_quantity']

        validate_available_seats(movie_show, seat_quantity)
        check_balance(movie_show, seat_quantity, customer=self.context['request'].user)

        return data
