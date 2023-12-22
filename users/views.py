from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from movie_shows.models import Order
from users.forms import RegisterForm
from users.models import Customer


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
    login_url = reverse_lazy('users:login')
    next_page = reverse_lazy('shows:show_list')


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'users/user_profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(customer=self.object).all()
        total_spent = Order.objects.filter(customer=self.object).aggregate(Sum('total_cost'))
        context['total_spent'] = total_spent['total_cost__sum']
        return context
