from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from movie_shows.models import CinemaHall, Movie, MovieShow, Order


class CinemaHallModelTest(TestCase):

    def test_cinema_hall_creation(self):
        hall = CinemaHall.objects.create(
                name='Test Hall',
                seats=100,
                screen_size=CinemaHall.LARGE,
                screen_type=CinemaHall.SCREEN_3D
        )
        self.assertIsInstance(hall, CinemaHall)
        self.assertEqual(hall.name, 'Test Hall')
        self.assertEqual(hall.seats, 100)
        self.assertEqual(hall.screen_size, CinemaHall.LARGE)
        self.assertEqual(hall.screen_type, CinemaHall.SCREEN_3D)

    def test_cinema_hall_str_representation(self):
        hall = CinemaHall.objects.create(
                name='Test Hall',
                seats=100,
                screen_size=CinemaHall.LARGE,
                screen_type=CinemaHall.SCREEN_3D
        )
        self.assertEqual(str(hall), 'Test Hall')

    def test_cinema_hall_absolute_url(self):
        hall = CinemaHall.objects.create(
                name='Test Hall',
                seats=100,
                screen_size=CinemaHall.LARGE,
                screen_type=CinemaHall.SCREEN_3D
        )
        expected_url = reverse('shows:hall_detail', args=[hall.id])
        self.assertEqual(hall.get_absolute_url(), expected_url)

    def test_cinema_hall_ordering(self):
        hall1 = CinemaHall.objects.create(name='Hall A', seats=150)
        hall2 = CinemaHall.objects.create(name='Hall B', seats=100)
        hall3 = CinemaHall.objects.create(name='Hall C', seats=200)

        halls = CinemaHall.objects.all()
        self.assertEqual(list(halls), [hall2, hall1, hall3])


class MovieModelTest(TestCase):

    def test_movie_creation(self):
        movie = Movie.objects.create(
                title='Test Movie',
                description='This is a test movie description.',
                duration_in_minutes=120,
                director='Test Director',
        )
        self.assertIsInstance(movie, Movie)
        self.assertEqual(movie.title, 'Test Movie')
        self.assertEqual(movie.description, 'This is a test movie description.')
        self.assertEqual(movie.duration_in_minutes, 120)
        self.assertEqual(movie.director, 'Test Director')

    def test_movie_str_representation(self):
        movie = Movie.objects.create(
                title='Test Movie',
                description='This is a test movie description.',
                duration_in_minutes=120,
                director='Test Director',
        )
        self.assertEqual(str(movie), 'Test Movie')

    def test_movie_default_poster(self):
        movie = Movie.objects.create(
                title='Test Movie',
                description='This is a test movie description.',
                duration_in_minutes=120,
                director='Test Director',
        )
        self.assertEqual(movie.poster.name, 'static/img/movie_poster.jpg')

    def test_movie_ordering(self):
        movie1 = Movie.objects.create(title='Movie A', duration_in_minutes=150)
        movie2 = Movie.objects.create(title='Movie B', duration_in_minutes=100)
        movie3 = Movie.objects.create(title='Movie C', duration_in_minutes=200)

        movies = Movie.objects.all()
        self.assertEqual(list(movies), [movie1, movie2, movie3])


class MovieShowModelTest(TestCase):

    def setUp(self):
        self.movie = Movie.objects.create(
                title='Test Movie',
                description='This is a test movie description.',
                duration_in_minutes=120,
                director='Test Director',
        )
        self.cinema_hall = CinemaHall.objects.create(
                name='Test Hall',
                seats=100,
                screen_size=CinemaHall.STANDARD,
                screen_type=CinemaHall.SCREEN_2D,
        )

    def test_movie_show_creation(self):
        movie_show = MovieShow.objects.create(
                movie=self.movie,
                movie_hall=self.cinema_hall,
                start_time='12:00',
                start_date='2023-01-01',
                end_time='14:00',
                end_date='2023-01-01',
                sold_seats=50,
                ticket_price='10.00',
        )
        self.assertIsInstance(movie_show, MovieShow)
        self.assertEqual(movie_show.movie, self.movie)
        self.assertEqual(movie_show.movie_hall, self.cinema_hall)
        self.assertEqual(str(movie_show), f'{self.movie} at 12:00')

    def test_movie_show_absolute_url(self):
        movie_show = MovieShow.objects.create(
                movie=self.movie,
                movie_hall=self.cinema_hall,
                start_time='12:00',
                start_date='2023-01-01',
                end_time='14:00',
                end_date='2023-01-01',
                sold_seats=50,
                ticket_price='10.00',
        )
        expected_url = reverse('shows:show_detail', args=[movie_show.id])
        self.assertEqual(movie_show.get_absolute_url(), expected_url)

    def test_movie_show_ordering(self):
        show1 = MovieShow.objects.create(
                movie=self.movie,
                movie_hall=self.cinema_hall,
                start_time='12:00',
                start_date='2023-01-03',
                end_time='14:00',
                end_date='2023-01-03',
                sold_seats=50,
                ticket_price='10.00',
        )
        show2 = MovieShow.objects.create(
                movie=self.movie,
                movie_hall=self.cinema_hall,
                start_time='14:00',
                start_date='2023-01-01',
                end_time='16:00',
                end_date='2023-01-01',
                sold_seats=30,
                ticket_price='12.00',
        )
        show3 = MovieShow.objects.create(
                movie=self.movie,
                movie_hall=self.cinema_hall,
                start_time='10:00',
                start_date='2023-01-02',
                end_time='12:00',
                end_date='2023-01-02',
                sold_seats=20,
                ticket_price='8.00',
        )

        shows = MovieShow.objects.all()
        self.assertEqual(list(shows), [show2, show3, show1])


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
                username='testuser',
                password='testpassword'
        )

        self.cinema_hall = CinemaHall.objects.create(
                name='Hall 1',
                seats=50,
                screen_size=CinemaHall.STANDARD,
                screen_type=CinemaHall.SCREEN_2D
        )

        self.movie = Movie.objects.create(
                title='Test Movie',
                description='A test movie',
                duration_in_minutes=120,
                director='Test Director'
        )

        self.movie_show = MovieShow.objects.create(
                movie=self.movie,
                movie_hall=self.cinema_hall,
                start_time='14:00:00',
                start_date='2023-01-01',
                end_time='16:00:00',
                end_date='2023-01-01',
                sold_seats=0,
                ticket_price=10.00
        )

    def test_order_creation(self):
        order = Order.objects.create(
                customer=self.user,
                movie_show=self.movie_show,
                seat_quantity=2,
                total_cost=20.00
        )

        self.assertEqual(order.customer, self.user)
        self.assertEqual(order.movie_show, self.movie_show)
        self.assertEqual(order.seat_quantity, 2)
        self.assertEqual(order.total_cost, 20.00)
        self.assertIsNotNone(order.ordered_at)

    def test_order_str_method(self):
        order = Order.objects.create(
                customer=self.user,
                movie_show=self.movie_show,
                seat_quantity=2,
                total_cost=20.00
        )

        expected_str = f'Order {order.id} by {self.user.username}'
        self.assertEqual(str(order), expected_str)
