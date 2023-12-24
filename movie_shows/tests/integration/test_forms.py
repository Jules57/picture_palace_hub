# from django.utils import timezone
#
# from movie_shows.forms import OrderCreateForm
# from movie_shows.models import CinemaHall, Movie, MovieShow
# from django.test import TestCase, RequestFactory
#
# from users.models import Customer
#
#
# class OrderCreateFormTest(TestCase):
#
#     def setUp(self):
#         self.factory = RequestFactory()
#
#         self.hall = CinemaHall.objects.create(
#                 name='Hall 1',
#                 seats=100,
#                 screen_size='Standard',
#                 screen_type='2D',
#         )
#         self.movie = Movie.objects.create(
#                 title='Movie 1',
#                 description='Description',
#                 duration_in_minutes=120,
#                 director='Director 1',
#         )
#         self.customer = Customer.objects.create(
#                 username='testuser',
#                 password='testpassword',
#                 balance=100.0
#         )
#         self.movie_show = MovieShow.objects.create(
#                 movie=self.movie,
#                 movie_hall=self.hall,
#                 start_time=timezone.now().time(),
#                 start_date=timezone.now().date(),
#                 end_time=(timezone.now() + timezone.timedelta(hours=2)).time(),
#                 end_date=(timezone.now() + timezone.timedelta(days=1)).date(),
#                 ticket_price=10.0,
#
#         )
#
#     def test_valid_form_data(self):
#         request = self.factory.get(f'cinema/shows/{self.movie_show.pk}/order/')
#         form_data = {
#             'seat_quantity': 2,
#             'movie_show': self.movie_show.pk,
#         }
#         form = OrderCreateForm(data=form_data, request=request)
#         self.assertTrue(form.is_valid())
#
#     def test_zero_seat_quantity(self):
#         request = self.factory.get(f'cinema/shows/{self.movie_show.pk}/order/')
#         form_data = {
#             'seat_quantity': 0,  # Invalid, should be at least 1
#             'movie_show': self.movie_show.pk,
#         }
#         form = OrderCreateForm(data=form_data, request=request)
#         self.assertFalse(form.is_valid())
#         self.assertIn('seat_quantity', form.errors)
#
#     def test_invalid_seat_quantity(self):
#         request = self.factory.get(f'cinema/shows/{self.movie_show.pk}/order/')
#         form_data = {
#             'seat_quantity': 150,  # Invalid, more than available seats
#             'movie_show': self.movie_show.pk,
#         }
#         form = OrderCreateForm(data=form_data, request=request)
#         self.assertFalse(form.is_valid())
#         self.assertIn('seat_quantity', form.errors)
#
#     def test_insufficient_balance(self):
#         request = self.factory.get(f'cinema/shows/{self.movie_show.pk}/order/')
#         request.user = Customer.objects.get(pk=1)
#         form_data = {
#             'seat_quantity': 2,
#             'movie_show': self.movie_show.pk,
#         }
#         # Decrease the user's balance to an insufficient amount
#         self.customer.balance = 5.0
#         self.customer.save()
#         form = OrderCreateForm(data=form_data, request=request)
#         self.assertFalse(form.is_valid())
#         self.assertIn(None, form.errors)
#
#     def test_negative_seat_quantity(self):
#         request = self.factory.get(f'cinema/shows/{self.movie_show.pk}/order/')
#         request.user = Customer.objects.get(pk=1)
#         form_data = {
#             'seat_quantity': -5,  # Invalid, should be positive
#             'movie_show': self.movie_show.pk,
#         }
#         form = OrderCreateForm(data=form_data, request=request)
#         self.assertFalse(form.is_valid())
#         self.assertIn('seat_quantity', form.errors)
