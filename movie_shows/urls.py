from django.urls import path, include

from movie_shows.views import CinemaHallCreateView, CinemaHallDetailView, CinemaHallListView, MovieShowListView, \
    MovieShowDetailView, MovieShowCreateView, MovieListView, CinemaHallUpdateView, CinemaHallDeleteView, \
    MovieShowUpdateView, MovieShowDeleteView, OrderCreateView

app_name = 'shows'

urlpatterns = [
    path('api/', include('movie_shows.api.urls')),
    path('hall/', CinemaHallListView.as_view(), name='hall_list'),
    path('hall/create/', CinemaHallCreateView.as_view(), name='create_hall'),
    path('hall/<int:pk>/', CinemaHallDetailView.as_view(), name='hall_detail'),
    path('hall/<int:pk>/edit/', CinemaHallUpdateView.as_view(), name='update_hall'),
    path('hall/<int:pk>/delete/', CinemaHallDeleteView.as_view(), name='delete_hall'),

    path('shows/', MovieShowListView.as_view(), name='show_list'),
    path('show/create/', MovieShowCreateView.as_view(), name='create_show'),
    path('show/<int:pk>/', MovieShowDetailView.as_view(), name='show_detail'),
    path('show/<int:pk>/delete/', MovieShowDeleteView.as_view(), name='delete_show'),
    path('show/<int:pk>/edit/', MovieShowUpdateView.as_view(), name='update_show'),

    path('show/<int:pk>/order/', OrderCreateView.as_view(), name='create_order'),

    path('movies/', MovieListView.as_view(), name='movie_list'),

]
