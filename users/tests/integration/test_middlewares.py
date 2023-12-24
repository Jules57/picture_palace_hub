from django.test import TestCase, Client

from django.urls import reverse
import datetime

from picture_palace_hub import settings
from users.models import Customer


class LogoutMiddlewareTestCase(TestCase):
    fixtures = ['fixtures/shows.json']

    def setUp(self):
        self.client = Client()

        self.user = Customer.objects.create(
                username='testuser',
                password='testpass',
                is_staff=False,
                is_superuser=False)
        self.client.force_login(self.user)

    def test_logout_after_timeout(self):
        # Set the last action time to a past time
        past_time = datetime.datetime.now() - datetime.timedelta(seconds=settings.TIME_SINCE_LAST_ACTION + 1)
        self.client.session['last_action'] = past_time.strftime("%H-%M-%S %d/%m/%y")

        # Make a request to trigger the middleware
        response = self.client.get(reverse('shows:create_order'))
        self.assertEqual(response.status_code, 200)  # Replace 200 with the expected status code

        # Check if the user is logged out
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_no_logout_before_timeout(self):
        # Set the last action time to a recent time
        recent_time = datetime.datetime.now() - datetime.timedelta(seconds=settings.TIME_SINCE_LAST_ACTION - 1)
        self.client.session['last_action'] = recent_time.strftime("%H-%M-%S %d/%m/%y")

        # Make a request to trigger the middleware
        response = self.client.get(reverse('shows:create_order'))  # Replace 'some_url' with the actual URL
        self.assertEqual(response.status_code, 200)  # Replace 200 with the expected status code

        # Check if the user is still logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)
