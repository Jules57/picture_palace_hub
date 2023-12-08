from django.contrib import admin

from users.models import Customer, Order, CustomerProfile


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'balance']
    list_filter = ['username', 'balance']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'movie_show', 'seat_quantity', 'total_cost']
    list_filter = ['customer', 'seat_quantity']
    search_fields = ['customer', 'movie_show']


@admin.register(CustomerProfile)
class CustomerProfile(admin.ModelAdmin):
    list_display = ['customer', 'total_spent']
