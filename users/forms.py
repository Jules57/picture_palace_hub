from django import forms

from users.models import Customer


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'password', 'image']
