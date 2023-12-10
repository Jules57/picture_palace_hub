from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from movie_shows.forms import CinemaHallCreateForm, MovieShowCreateForm
from movie_shows.mixins import AdminRequiredMixin
from movie_shows.models import CinemaHall, MovieShow, Movie


class MovieListView(ListView):
    model = Movie
    template_name = 'movie_shows/movies/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 2
    ordering = ['-title']


class CinemaHallDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('users:login')
    model = CinemaHall
    template_name = 'movie_shows/halls/hall_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shows'] = self.object.shows.all().order_by('-start_date')
        return context


class CinemaHallUpdateView(AdminRequiredMixin, UpdateView):
    model = CinemaHall
    fields = ['name', 'seats', 'screen_size', 'screen_type']
    http_method_names = ['get', 'post']
    login_url = reverse_lazy('users:login')
    template_name = 'movie_shows/halls/hall_update.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class CinemaHallListView(ListView):
    model = CinemaHall
    template_name = 'movie_shows/halls/hall_list.html'
    paginate_by = 5
    context_object_name = 'halls'


class CinemaHallDeleteView(AdminRequiredMixin, DeleteView):
    login_url = reverse_lazy('users:login')
    model = CinemaHall
    success_url = reverse_lazy('shows:hall_list')
    template_name = 'movie_shows/halls/hall_delete.html'


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
    ordering = ['-start_time']

    def get_queryset(self):
        sort_by_time = self.request.GET.get('sort_by', 'start_time')
        sort_by_price = self.request.GET.get('sort_by', 'ticket_price')
        # sort_order = self.request.GET.get('sort_order', 'asc')

        # if sort_order not in ['asc', 'desc']:
        #     sort_order = 'asc'

        if sort_by_time:
            queryset = MovieShow.objects.order_by(sort_by_time)
        else:
            queryset = MovieShow.objects.order_by(f'-{sort_by_price}')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_by_time'] = self.request.GET.get('sort_by', 'start_time')
        context['sort_by_price'] = self.request.GET.get('sort_by', 'ticket_price')
        return context


class MovieShowDetailView(DetailView):
    context_object_name = 'show'
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

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['error_message'] = 'Invalid form data'
        return self.render_to_response(context)





# class MovieShowUpdateView(AdminRequiredMixin, UpdateView):
#     model = MovieShow
#     fields = ['movie', 'movie_hall', 'start_date', 'start_time', 'end_time', 'price']
#     http_method_names = ['get', 'post']
#     login_url = reverse_lazy('users:login')
#     template_name = 'movie_shows/shows/show_update.html'
