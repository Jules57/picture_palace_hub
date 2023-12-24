from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone

from movie_shows.forms import CinemaHallCreateForm, MovieShowCreateForm, OrderCreateForm
from movie_shows.models import CinemaHall, Movie, MovieShow



class CinemaHallCreateFormTest(TestCase):

    def test_valid_form_data(self):
        form_data = {
            'name': 'Hall 1',
            'seats': 100,
            'screen_size': 'Standard',
            'screen_type': '2D',
        }
        form = CinemaHallCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_data(self):
        form_data = {
            'name': 'Hall 1',
            'seats': -10,
            'screen_size': 'Standard',
            'screen_type': '2D',
        }
        form = CinemaHallCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('seats', form.errors)


class MovieShowCreateFormTest(TestCase):

    def setUp(self):
        self.hall = CinemaHall.objects.create(
                name='Hall 1',
                seats=100,
                screen_size='Standard',
                screen_type='2D',
        )
        self.movie = Movie.objects.create(
                title='Movie 1',
                description='Description',
                duration_in_minutes=120,
                director='Director 1',
        )

    def test_valid_form_data(self):
        form_data = {
            'movie': self.movie.pk,
            'movie_hall': self.hall.pk,
            'start_date': timezone.now().date(),
            'start_time': (timezone.now() + timedelta(hours=1)).time(),
            'end_date': (timezone.now() + timedelta(days=1)).date(),
            'end_time': (timezone.now() + timedelta(days=1, hours=2)).time(),
            'ticket_price': 10.0,
        }
        form = MovieShowCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_data(self):
        form_data = {
            'movie': self.movie.pk,
            'movie_hall': self.hall.pk,
            'start_date': timezone.now().date(),
            'start_time': (timezone.now() + timedelta(hours=1)).time(),
            'end_date': timezone.now().date(),  # Invalid end date
            'end_time': (timezone.now() + timedelta(hours=2)).time(),
            'ticket_price': 10.0,
        }
        form = MovieShowCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('start_date', form.errors)


# class OrderCreateFormTest(TestCase):
#
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = get_user_model().objects.create_user(
#             username='testuser',
#             password='testpassword'
#         )
#         self.hall = CinemaHall.objects.create(
#             name='Hall 1',
#             seats=100,
#             screen_size='Standard',
#             screen_type='2D',
#         )
#         self.movie = Movie.objects.create(
#             title='Movie 1',
#             description='Description',
#             duration_in_minutes=120,
#             director='Director 1',
#         )
#         self.movie_show = MovieShow.objects.create(
#             movie=self.movie,
#             movie_hall=self.hall,
#             start_time=timezone.now().time(),
#             start_date=timezone.now().date(),
#             end_time=(timezone.now() + timezone.timedelta(hours=2)).time(),
#             end_date=(timezone.now() + timezone.timedelta(days=1)).date(),
#             ticket_price=10.0,
#         )
#
#     def test_order_create_form(self):
#         data = {
#             'seat_quantity': 2,  # Adjust values as needed
#             'movie_show': self.movie_show.id,
#         }
#         request = self.factory.post(reverse('shows:show_detail', kwargs={'pk': self.movie_show.pk}), data)
#         request.user = self.user
#
#         form = OrderCreateForm(data, request=request)
#         self.assertTrue(form.is_valid())
#
#         # Now you can check the messages
#         response = self.client.post(reverse('shows:show_detail', kwargs={'pk': self.movie_show.pk}), data)
#         messages = list(get_messages(response.request))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), "Your success message goes here")
#
#     def test_valid_form_data(self):
#         form_data = {
#             'seat_quantity': 2,
#             'movie_show': self.movie_show.pk,
#         }
#         form = OrderCreateForm(data=form_data)
#         self.assertTrue(form.is_valid())
#
#     def test_zero_seat_quantity(self):
#         form_data = {
#             'seat_quantity': 0,  # Invalid, should be at least 1
#             'movie_show': self.movie_show.pk,
#         }
#         form = OrderCreateForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('seat_quantity', form.errors)
#
#     def test_invalid_seat_quantity(self):
#         form_data = {
#             'seat_quantity': 150,  # Invalid, more than available seats
#             'movie_show': self.movie_show.pk,
#         }
#         form = OrderCreateForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('seat_quantity', form.errors)
