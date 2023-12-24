from datetime import timedelta

from django.http import Http404
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from django.utils import timezone

from movie_shows.forms import OrderCreateForm
from movie_shows.models import CinemaHall, MovieShow, Movie
from movie_shows.views import CinemaHallDetailView, CinemaHallUpdateView, CinemaHallDeleteView, MovieShowDetailView, \
    MovieShowListView


class CinemaHallDetailViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
                username='testuser',
                password='testpassword'
        )
        self.cinema_hall = CinemaHall.objects.create(
                name='Test Hall',
                seats=100,
                screen_size=CinemaHall.STANDARD,
                screen_type=CinemaHall.SCREEN_2D
        )
        self.movie = Movie.objects.create(
                title='Test Movie',
                description='This is a test movie description.',
                duration_in_minutes=120,
                director='Test Director',
        )
        self.movie_show = MovieShow.objects.create(
                movie=self.movie,
                movie_hall=self.cinema_hall,
                start_time='12:00',
                start_date='2023-01-01',
                end_time='14:00',
                end_date='2023-01-01',
                sold_seats=50,
                ticket_price='10.00',
        )

    def test_get_context_data_shows_ordered_by_start_date(self):
        request = self.factory.get(reverse('shows:hall_detail', kwargs={'pk': self.cinema_hall.pk}))
        request.user = self.user
        view = CinemaHallDetailView.as_view()
        response = view(request, pk=self.cinema_hall.pk)
        context = response.context_data
        self.assertIn('shows', context)
        self.assertEqual(list(context['shows']), [self.movie_show])

    def test_get_context_data_no_shows(self):
        request = self.factory.get(reverse('shows:hall_detail', kwargs={'pk': self.cinema_hall.pk}))
        request.user = self.user

        cinema_hall_without_shows = CinemaHall.objects.create(
                name='Empty Hall',
                seats=50,
                screen_size=CinemaHall.LARGE,
                screen_type=CinemaHall.SCREEN_3D
        )

        view = CinemaHallDetailView.as_view()
        response = view(request, pk=cinema_hall_without_shows.pk)
        context = response.context_data
        self.assertIn('shows', context)
        self.assertEqual(list(context['shows']), [])

    def test_get_context_data_invalid_hall_id(self):
        request = self.factory.get(reverse('shows:hall_detail', kwargs={'pk': 999}))  # Non-existent hall id
        request.user = self.user
        view = CinemaHallDetailView.as_view()
        with self.assertRaises(Http404):
            response = view(request, pk=999)


class CinemaHallListViewTestCase(TestCase):
    def setUp(self):
        CinemaHall.objects.create(name='Hall 1', seats=50, screen_size='Standard', screen_type='2D')
        CinemaHall.objects.create(name='Hall 2', seats=60, screen_size='Premium', screen_type='3D')
        CinemaHall.objects.create(name='Hall 3', seats=70, screen_size='Large', screen_type='2D')
        CinemaHall.objects.create(name='Hall 4', seats=80, screen_size='Standard', screen_type='3D')
        CinemaHall.objects.create(name='Hall 5', seats=90, screen_size='Premium', screen_type='2D')

        self.url = reverse('shows:hall_list')

    def test_cinema_hall_list_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['halls']), 5)

        self.assertContains(response, 'Hall 1')
        self.assertContains(response, 'Hall 2')
        self.assertContains(response, 'Hall 3')
        self.assertContains(response, 'Hall 4')
        self.assertContains(response, 'Hall 5')

        self.assertEqual(response.context['halls'].count(), 5)

    def test_empty_cinema_hall_list_view(self):
        CinemaHall.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['halls']), 0)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/cinema/hall/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('shows:hall_list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('shows:hall_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'movie_shows/halls/hall_list.html')


class CinemaHallUpdateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
                username='adminuser',
                password='adminpassword',
                is_staff=True
        )
        self.cinema_hall = CinemaHall.objects.create(
                name='Test Hall',
                seats=100,
                screen_size=CinemaHall.LARGE,
                screen_type=CinemaHall.SCREEN_2D
        )

    def test_get_success_url(self):
        request = self.factory.get(reverse('shows:update_hall', kwargs={'pk': self.cinema_hall.pk}))
        request.user = self.user
        view = CinemaHallUpdateView()
        view.setup(request, pk=self.cinema_hall.pk)
        view.object = self.cinema_hall
        success_url = view.get_success_url()
        expected_url = reverse('shows:hall_detail', kwargs={'pk': self.cinema_hall.pk})
        self.assertEqual(success_url, expected_url)


class CinemaHallDeleteViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
                username='adminuser',
                password='adminpassword',
                is_staff=True
        )
        self.cinema_hall = CinemaHall.objects.create(
                name='Test Hall',
                seats=100,
                screen_size=CinemaHall.LARGE,
                screen_type=CinemaHall.SCREEN_2D
        )

    def test_get_success_url(self):
        request = self.factory.get(reverse('shows:delete_hall', kwargs={'pk': self.cinema_hall.pk}))
        request.user = self.user
        view = CinemaHallDeleteView()
        view.setup(request, pk=self.cinema_hall.pk)
        view.object = self.cinema_hall
        success_url = view.get_success_url()
        expected_url = reverse('shows:hall_list')
        self.assertEqual(success_url, expected_url)


class MovieShowDetailViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
                username='testuser',
                password='testpassword'
        )
        self.cinema_hall = CinemaHall.objects.create(
                name='Test Hall',
                seats=100,
                screen_size=CinemaHall.LARGE,
                screen_type=CinemaHall.SCREEN_2D
        )
        self.movie = Movie.objects.create(
                title='Test Movie',
                description='This is a test movie description.',
                duration_in_minutes=120,
                director='Test Director',
        )
        self.movie_show = MovieShow.objects.create(
                movie=self.movie,
                movie_hall=self.cinema_hall,
                start_time='12:00',
                start_date='2023-01-01',
                end_time='14:00',
                end_date='2023-01-01',
                sold_seats=10,
                ticket_price=10.00
        )


    def test_get_context_data_available_seats(self):
        request = self.factory.get(reverse('shows:show_detail', kwargs={'pk': self.movie_show.pk}))
        request.user = self.user
        view = MovieShowDetailView()
        view.setup(request, pk=self.movie_show.pk)
        view.object = self.movie_show
        context = view.get_context_data()
        expected_available_seats = self.cinema_hall.seats - self.movie_show.sold_seats
        self.assertEqual(context['available_seats'], expected_available_seats)

    def test_get_context_data_order_form(self):
        request = self.factory.get(reverse('shows:show_detail', kwargs={'pk': self.movie_show.pk}))
        request.user = self.user
        view = MovieShowDetailView()
        view.setup(request, pk=self.movie_show.pk)
        view.object = self.movie_show
        context = view.get_context_data()
        self.assertIsInstance(context['order_form'], OrderCreateForm)
        self.assertEqual(context['order_form'].initial['movie_show'], self.movie_show)

    def test_get_context_data_default(self):
        request = self.factory.get(reverse('shows:show_detail', kwargs={'pk': self.movie_show.pk}))
        request.user = self.user
        view = MovieShowDetailView()
        view.setup(request, pk=self.movie_show.pk)
        view.object = self.movie_show
        context = view.get_context_data()
        self.assertIn('show', context)
        self.assertIn('available_seats', context)
        self.assertIn('order_form', context)


class MovieShowListViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.cinema_hall = CinemaHall.objects.create(
                name='Test Hall',
                seats=100,
                screen_size=CinemaHall.LARGE,
                screen_type=CinemaHall.SCREEN_2D
        )
        self.movie = Movie.objects.create(
                title='Test Movie',
                description='This is a test movie description.',
                duration_in_minutes=120,
                director='Test Director',
        )
        self.user = get_user_model().objects.create_user(
                username='testuser',
                password='testpassword'
        )

    def create_movie_show(self, start_date, start_time, end_date, end_time, ticket_price):
        return MovieShow.objects.create(
                movie=self.movie,
                movie_hall=self.cinema_hall,
                start_time=start_time,
                start_date=start_date,
                end_time=end_time,
                end_date=end_date,
                ticket_price=ticket_price
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/cinema/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('shows:show_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('shows:show_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'movie_shows/shows/show_list.html')

    def test_get_queryset_default(self):
        request = self.factory.get(reverse('shows:show_list'))
        request.user = self.user
        view = MovieShowListView()
        view.setup(request)
        queryset = view.get_queryset()
        self.assertEqual(queryset.query.order_by, ('-start_time', '-ticket_price'))

    def test_get_context_data_default(self):
        request = self.factory.get(reverse('shows:show_list'))
        request.user = self.user
        queryset = MovieShow.objects.all()
        view = MovieShowListView()
        view.setup(request, queryset)
        context = view.get_context_data(object_list=queryset)
        self.assertIn('shows', context)

    def test_get_queryset_today_filter(self):
        today = timezone.now().date()
        self.create_movie_show(today, '12:00', today, '14:00', 10.00)
        request = self.factory.get(reverse('shows:show_list'), {'day': 'today'})
        request.user = self.user
        view = MovieShowListView()
        view.setup(request)
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 1)

    def test_get_queryset_next_day_filter(self):
        next_day = timezone.now().date() + timedelta(days=1)
        self.create_movie_show(next_day, '12:00', next_day, '14:00', 10.00)

        request = self.factory.get(reverse('shows:show_list'), {'day': 'next_day'})
        request.user = self.user
        view = MovieShowListView()
        view.setup(request)
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 1)
