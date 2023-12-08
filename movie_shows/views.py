from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from movie_shows.forms import CinemaHallCreateForm, MovieShowCreateForm
from movie_shows.models import CinemaHall, MovieShow, Movie


class AdminRequiredMixin(UserPassesTestMixin, AccessMixin):
    def test_func(self):
        return self.request.user.is_superuser


class CinemaHallDetailView(LoginRequiredMixin, DetailView):
    model = CinemaHall
    template_name = 'movie_shows/halls/hall_detail.html'


class CinemaHallUpdateView(AdminRequiredMixin, UpdateView):
    model = CinemaHall
    fields = ['name', 'seats', 'screen_size', 'screen_type']
    http_method_names = ['get', 'post']
    login_url = reverse_lazy('users:login')
    template_name = 'movie_shows/halls/hall_update.html'
    success_url = reverse_lazy('shows:hall_list')


class CinemaHallListView(ListView):
    model = CinemaHall
    template_name = 'movie_shows/halls/hall_list.html'
    paginate_by = 5
    context_object_name = 'halls'


class CinemaHallCreateView(AdminRequiredMixin, CreateView):
    model = CinemaHall
    pk_url_kwarg = 'pk'
    form_class = CinemaHallCreateForm
    http_method_names = ['get', 'post']
    login_url = reverse_lazy('users:login')
    template_name = 'movie_shows/halls/hall_create.html'
    success_url = reverse_lazy('shows:hall_list')


class MovieShowListView(ListView):
    model = MovieShow
    template_name = 'movie_shows/shows/show_list.html'
    context_object_name = 'shows'
    paginate_by = 10
    ordering = ['start_time']


class MovieShowDetailView(DetailView):
    model = MovieShow
    template_name = 'movie_shows/shows/show_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['available_seats'] = self.object.movie_hall.seats - self.object.sold_seats
        return context


class MovieShowCreateView(AdminRequiredMixin, CreateView):
    model = MovieShow
    pk_url_kwarg = 'pk'
    form_class = MovieShowCreateForm
    http_method_names = ['get', 'post']
    login_url = reverse_lazy('users:login')
    template_name = 'movie_shows/shows/show_create.html'


class MovieListView(ListView):
    model = Movie
    template_name = 'movie_shows/movies/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 2
    ordering = ['-title']
