from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from movie_shows.forms import CinemaHallCreateForm, MovieShowCreateForm, OrderCreateForm
from movie_shows.mixins import AdminRequiredMixin, SoldTicketCheckMixin
from movie_shows.models import CinemaHall, MovieShow, Movie, Order


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


class CinemaHallUpdateView(AdminRequiredMixin, SoldTicketCheckMixin, UpdateView):
    model = CinemaHall
    http_method_names = ['get', 'post']
    login_url = reverse_lazy('users:login')
    template_name = 'movie_shows/halls/hall_update.html'
    fields = ['name', 'seats', 'screen_size', 'screen_type']

    def get_success_url(self):
        messages.success(self.request, f'{self.object.name} has been updated.')
        return self.object.get_absolute_url()


class CinemaHallListView(ListView):
    model = CinemaHall
    template_name = 'movie_shows/halls/hall_list.html'
    paginate_by = 5
    context_object_name = 'halls'


class CinemaHallDeleteView(AdminRequiredMixin, SoldTicketCheckMixin, DeleteView):
    login_url = reverse_lazy('users:login')
    model = CinemaHall
    template_name = 'movie_shows/halls/hall_delete.html'

    def get_success_url(self):
        messages.success(self.request, f'{self.object.name} has been deleted.')
        return reverse_lazy('shows:hall_list')


class CinemaHallCreateView(AdminRequiredMixin, CreateView):
    model = CinemaHall
    pk_url_kwarg = 'pk'
    form_class = CinemaHallCreateForm
    http_method_names = ['get', 'post']
    login_url = reverse_lazy('users:login')
    template_name = 'movie_shows/halls/hall_create.html'
    success_url = reverse_lazy('shows:hall_list')

    def get_success_url(self):
        messages.success(self.request, f'{self.object.name} has been created successfully.')
        return self.object.get_absolute_url()


class MovieShowListView(ListView):
    model = MovieShow
    template_name = 'movie_shows/shows/show_list.html'
    context_object_name = 'shows'
    paginate_by = 3

    def get_queryset(self):
        queryset = MovieShow.objects.all()

        sort_by = self.request.GET.get('sort_by', 'start_time')
        sort_order = self.request.GET.get('sort_order', 'asc')
        day = self.request.GET.get('day', None)

        if sort_order == 'asc':
            queryset = queryset.order_by(sort_by, 'ticket_price')
        else:
            queryset = queryset.order_by(f'-{sort_by}', '-ticket_price')

        if day == 'today':
            today = timezone.now().date()
            queryset = queryset.filter(
                    start_date__lte=today,
                    end_date__gte=today
            )
        elif day == 'next_day':
            next_day = timezone.now().date() + timedelta(days=1)
            queryset = queryset.filter(
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


class MovieShowDetailView(DetailView):
    context_object_name = 'show'
    model = MovieShow
    http_method_names = ['get', 'post']
    template_name = 'movie_shows/shows/show_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['available_seats'] = self.object.movie_hall.seats - self.object.sold_seats
        context['order_form'] = OrderCreateForm(initial={'movie_show': self.object})
        return context


class MovieShowCreateView(AdminRequiredMixin, CreateView):
    login_url = reverse_lazy('users:login')
    model = MovieShow
    form_class = MovieShowCreateForm
    template_name = 'movie_shows/shows/show_create.html'
    success_url = reverse_lazy('shows:show_list')

    def get_absolute_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Movie show has been created successfully.")
        return self.object.get_absolute_url()


class MovieShowUpdateView(AdminRequiredMixin, SoldTicketCheckMixin, UpdateView):
    login_url = reverse_lazy('users:login')
    model = MovieShow
    form_class = MovieShowCreateForm
    template_name = 'movie_shows/shows/show_update.html'

    def get_success_url(self):
        return reverse_lazy('shows:show_list')


class MovieShowDeleteView(AdminRequiredMixin, SoldTicketCheckMixin, DeleteView):
    login_url = reverse_lazy('users:login')
    model = MovieShow
    http_method_names = ['get', 'post']
    template_name = 'movie_shows/shows/show_delete.html'

    def get_success_url(self):
        return reverse_lazy('shows:show_list')


class OrderCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('users:login')
    model = Order
    form_class = OrderCreateForm
    http_method_names = ['get', 'post']

    def get_success_url(self):
        movie_show = self.object.movie_show
        return movie_show.get_absolute_url()

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'movie_show_id': self.kwargs.get('pk')})
        return kwargs

    def form_valid(self, form):
        order = form.save(commit=False)
        seat_quantity = form.cleaned_data['seat_quantity']
        movie_show = form.cleaned_data['movie_show']

        movie_show.sold_seats += seat_quantity
        order.total_cost = seat_quantity * movie_show.ticket_price
        order.customer = form.request.user
        order.movie_show = movie_show

        order.customer.balance -= order.total_cost

        with transaction.atomic():
            order.save()
            order.customer.save()
            movie_show.save()
        messages.success(self.request, "Order successful!")
        return super().form_valid(form=form)

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse_lazy('shows:show_detail', kwargs={'pk': self.kwargs.get('pk')}))
