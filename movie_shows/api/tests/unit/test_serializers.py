from django.test import TestCase

from movie_shows.api.serializers import MovieReadSerializer, MovieShowReadSerializer, MovieShowWriteSerializer, \
    CinemaHallReadSerializer, CinemaHallWriteSerializer
from movie_shows.models import Movie, CinemaHall, MovieShow


class MovieReadSerializerTest(TestCase):
    def setUp(self):
        self.movie_data = {
            'id': 1,
            'title': 'Test Movie',
            'description': 'This is a test movie.',
            'duration_in_minutes': 120,
            'director': 'Test Director',
        }
        self.movie_instance = Movie.objects.create(**self.movie_data)
        self.serializer = MovieReadSerializer(instance=self.movie_instance)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'title', 'description', 'duration_in_minutes', 'director'})

    def test_serializer_data_matches_movie_instance(self):
        data = self.serializer.data
        for key, value in self.movie_data.items():
            self.assertEqual(data[key], value)


class MovieShowReadSerializerTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
                title='Test Movie',
                description='This is a test movie.',
                duration_in_minutes=120,
                director='Test Director'
        )

        self.cinema_hall = CinemaHall.objects.create(
                name='Test Hall',
                seats=100,
                screen_size='Standard',
                screen_type='2D'
        )

        self.movie_show_data = {
            'id': 1,
            'movie': self.movie,
            'movie_hall': self.cinema_hall,
            'start_time': '12:00:00',
            'start_date': '2023-12-25',
            'end_time': '14:30:00',
            'end_date': '2023-12-25',
            'sold_seats': 10,
            'ticket_price': '15.00'
        }

        self.movie_show_instance = MovieShow.objects.create(**self.movie_show_data)
        self.serializer = MovieShowReadSerializer(instance=self.movie_show_instance)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = ['id', 'movie', 'movie_hall', 'start_time', 'start_date', 'end_time', 'end_date',
                           'sold_seats', 'ticket_price']
        self.assertEqual(set(data.keys()), set(expected_fields))

    def test_serializer_data_matches_movie_show_instance(self):
        data = self.serializer.data
        for key, value in self.movie_show_data.items():
            if key in ['movie', 'movie_hall']:
                self.assertEqual(data[key], str(value))
            else:
                self.assertEqual(data[key], value)


class MovieShowWriteSerializerTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
                title='Test Movie',
                description='This is a test movie.',
                duration_in_minutes=120,
                director='Test Director'
        )

        self.cinema_hall = CinemaHall.objects.create(
                name='Test Hall',
                seats=100,
                screen_size='Standard',
                screen_type='2D'
        )

        self.movie_show_data = {
            'movie': self.movie.id,
            'movie_hall': self.cinema_hall.id,
            'start_time': '12:00:00',
            'start_date': '2023-12-25',
            'end_time': '14:30:00',
            'end_date': '2023-12-28',
            'sold_seats': 0,
            'ticket_price': '15.00'
        }

        self.serializer = MovieShowWriteSerializer(data=self.movie_show_data)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.initial_data
        expected_fields = ['movie', 'movie_hall', 'start_time', 'start_date', 'end_time', 'end_date',
                           'sold_seats', 'ticket_price']
        self.assertEqual(set(data.keys()), set(expected_fields))

    def test_serializer_is_valid(self):
        self.assertTrue(self.serializer.is_valid(), self.serializer.errors)


class CinemaHallReadSerializerTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
                title='Test Movie',
                description='A test movie description',
                duration_in_minutes=120,
                director='Test Director'
        )

        self.cinema_hall = CinemaHall.objects.create(
                name='Test Hall',
                seats=50,
                screen_size='Standard',
                screen_type='2D'
        )

        self.movie_show = MovieShow.objects.create(
                movie=self.movie,
                movie_hall=self.cinema_hall,
                start_time='12:00:00',
                start_date='2023-12-25',
                end_time='14:30:00',
                end_date='2023-12-25',
                sold_seats=10,
                ticket_price='15.00'
        )

        self.serializer_data = {
            'id': self.cinema_hall.id,
            'name': 'Test Hall',
            'seats': 50,
            'screen_size': 'Standard',
            'screen_type': '2D',
            'shows': [{
                'id': self.movie_show.id, 'movie': 'Test Movie', 'movie_hall': 'Test Hall',
                'start_time': '12:00:00',
                'start_date': '2023-12-25', 'end_time': '14:30:00', 'end_date': '2023-12-25',
                'sold_seats': 10,
                'ticket_price': '15.00'}]
        }

        self.serializer = CinemaHallReadSerializer(instance=self.cinema_hall)

    def test_serializer_contains_expected_fields(self):
        expected_fields = {'id', 'name', 'seats', 'screen_size', 'screen_type', 'shows'}
        self.assertEqual(set(self.serializer.data.keys()), expected_fields)

    def test_serializer_data_matches_input_data(self):
        self.assertEqual(self.serializer.data, self.serializer_data)


class CinemaHallWriteSerializerTests(TestCase):
    def setUp(self):
        self.cinema_hall = CinemaHall.objects.create(
                name='Test Hall',
                seats=50,
                screen_size='Standard',
                screen_type='2D'
        )

        self.serializer_data = {
            'name': 'Updated Hall',
            'seats': 60,
            'screen_size': 'Premium',
            'screen_type': '3D'
        }

        self.serializer = CinemaHallWriteSerializer(instance=self.cinema_hall, data=self.serializer_data)

    def test_serializer_contains_expected_fields(self):
        expected_fields = {'name', 'seats', 'screen_size', 'screen_type'}
        self.assertEqual(set(self.serializer.initial_data.keys()), expected_fields)

    def test_serializer_data_is_valid(self):
        self.assertTrue(self.serializer.is_valid())

    def test_serializer_data_matches_input_data(self):
        self.assertTrue(self.serializer.is_valid())
        validated_data = self.serializer.validated_data
        for key, value in self.serializer_data.items():
            self.assertEqual(validated_data[key], value)
