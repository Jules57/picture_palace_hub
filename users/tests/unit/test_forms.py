from django.test import TestCase
from django.urls import reverse


class RegisterFormTest(TestCase):

    def test_valid_form_submission(self):
        data = {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
        }

        response = self.client.post(reverse('users:register'), data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_form_submission(self):
        data = {
            'username': '',  # Invalid because it's an empty string
            'password1': 'short',  # Invalid because it's too short
            'password2': 'mismatch',  # Invalid because it doesn't match 'password1'
        }

        response = self.client.post(reverse('users:register'), data)
        self.assertEqual(response.status_code, 200)  # the form renders the same page with errors
