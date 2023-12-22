from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from users.forms import RegisterForm


class RegisterViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('users:register')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_register.html')
        self.assertIsInstance(response.context['form'], RegisterForm)

    def test_register_view_post_success(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('shows:show_list'))

    def test_register_view_post_failure(self):
        data = {
            'username': '',
            'password1': 'password',
            'password2': 'different_password',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_register.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)


class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('users:login')

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_login_view_post_success(self):
        user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('shows:show_list'))

    def test_login_view_post_failure(self):
        data = {
            'username': 'nonexistentuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_login.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)


class LogoutViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('users:logout')
        self.show_list_url = reverse('shows:show_list')

    def test_logout_view(self):
        user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)

        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.show_list_url)
