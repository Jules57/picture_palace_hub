from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import RegisterForm


class RegisterView(CreateView):
    template_name = 'users/user_register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('shows:show_list')


class Login(LoginView):
    success_url = reverse_lazy('shows:show_list')
    template_name = 'users/user_login.html'

    def get_success_url(self):
        return self.success_url


class Logout(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('users:login')
