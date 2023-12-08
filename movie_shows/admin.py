from django.contrib import admin

from movie_shows.models import Movie, CinemaHall, MovieShow


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'duration_in_minutes', 'poster']
    list_filter = ['id', 'title', 'duration_in_minutes']
    search_fields = ['title']


@admin.register(CinemaHall)
class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'seats', 'screen_size', 'screen_type']
    list_filter = ['name', 'seats']
    search_fields = ['name', 'seats']


@admin.register(MovieShow)
class MovieShowAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie', 'movie_hall', 'start_time', 'start_date',
                    'end_time', 'end_date', 'sold_seats', 'ticket_price']
    list_filter = ['movie', 'movie_hall', 'start_time', 'start_date',
                   'end_time', 'end_date', 'sold_seats', 'ticket_price']
    search_fields = ['movie', 'movie_hall']
    list_editable = ['start_time', 'end_time', 'start_date', 'end_date', 'ticket_price']
