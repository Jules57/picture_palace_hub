from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from movie_shows import exceptions
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
    paginate_by = 3
    ordering = ['-start_time']

    def get_queryset(self):
        queryset = MovieShow.objects.all()

        sort_by = self.request.GET.get('sort_by', 'start_time')
        sort_order = self.request.GET.get('sort_order', 'asc')
        day = self.request.GET.get('day', None)

        if sort_order not in ['asc', 'desc']:
            sort_order = 'asc'

        if sort_order == 'asc':
            queryset = queryset.order_by(sort_by, 'ticket_price')
        else:
            queryset = queryset.order_by(f'-{sort_by}', '-ticket_price')

        if day == 'today':
            today = timezone.now().date()
            queryset = MovieShow.objects.filter(
                    start_date__lte=today,
                    end_date__gte=today
            )
        elif day == 'next_day':
            next_day = timezone.now().date() + timedelta(days=1)
            queryset = MovieShow.objects.filter(
                    start_date__lte=next_day,
                    end_date__gte=next_day
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_by'] = self.request.GET.get('sort_by', 'start_time')
        context['sort_order'] = self.request.GET.get('sort_order', 'asc')
        context['day'] = self.request.GET.get('day', None)

        return context


class NextDayMovieShowListView(ListView):
    model = MovieShow
    template_name = 'movie_shows/shows/show_list.html'
    context_object_name = 'shows'
    paginate_by = 3
    ordering = ['start_time']

    def get_queryset(self):
        queryset = super().get_queryset()
        today = timezone.today()
        today_shows = MovieShow.objects.filter(
                start_date__lte=today,
                end_date__gte=today
        )
        return queryset


class MovieShowDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('users:login')
    context_object_name = 'show'
    model = MovieShow
    template_name = 'movie_shows/shows/show_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['available_seats'] = self.object.movie_hall.seats - self.object.sold_seats
        return context


class MovieShowCreateView(AdminRequiredMixin, CreateView):
    login_url = reverse_lazy('users:login')
    model = MovieShow
    form_class = MovieShowCreateForm
    template_name = 'movie_shows/shows/show_create.html'
    success_url = reverse_lazy('shows:show_list')

    def form_valid(self, form):
        try:
            form.save()
        except exceptions.MovieShowsCollideException:
            messages.add_message(self.request, messages.ERROR, "This movie show collides with another show.")
            return HttpResponseRedirect(self.request.path_info)
        else:
            messages.add_message(self.request, messages.SUCCESS, "Movie show has been created successfully.")
            return HttpResponseRedirect(self.success_url)


class MovieShowUpdateView(AdminRequiredMixin, UpdateView):
    login_url = reverse_lazy('users:login')
    model = MovieShow
    fields = ['movie', 'movie_hall', 'start_time', 'end_time', 'start_date', 'end_date', 'ticket_price']
    template_name = 'movie_shows/shows/show_update.html'


class MovieShowDeleteView(AdminRequiredMixin, DeleteView):
    login_url = reverse_lazy('users:login')
    model = MovieShow
    success_url = reverse_lazy('shows:show_list')
    template_name = 'movie_shows/shows/show_delete.html'
