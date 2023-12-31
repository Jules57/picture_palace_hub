from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from users.forms import RegisterForm
from users.models import Customer
from users.views import Login


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

    def test_get_success_url(self):
        login_view = Login()
        success_url = login_view.get_success_url()
        self.assertEqual(success_url, reverse('shows:show_list'))


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


class CustomerDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = Customer.objects.create_user(username='testuser', password='testpass')
        self.url = reverse('users:profile', kwargs={'pk': self.user.pk})

    def test_customer_detail_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)
        self.assertIn('orders', response.context)
        self.assertIn('total_spent', response.context)

    def test_customer_detail_view_with_no_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login') + '?next=' + self.url)
