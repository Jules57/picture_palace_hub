from django.contrib import admin

from movie_shows.models import Order
from users.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'balance']
    list_filter = ['username', 'balance']
