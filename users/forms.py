from django.contrib.auth.forms import UserCreationForm

from users.models import Customer


class RegisterForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', ]
