from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from movie_shows import exceptions
from movie_shows.forms import CinemaHallCreateForm, MovieShowCreateForm, OrderCreateForm, CinemaHallUpdateForm
from movie_shows.mixins import AdminRequiredMixin
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


class CinemaHallUpdateView(AdminRequiredMixin, UpdateView):
    model = CinemaHall
    form_class = CinemaHallUpdateForm
    http_method_names = ['get', 'post']
    login_url = reverse_lazy('users:login')
    template_name = 'movie_shows/halls/hall_update.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def get_success_url(self):
        return self.object.get_absolute_url()

    # def form_valid(self, form):
    #     try:
    #         form.save()
    #     except exceptions.SeatsSoldException:
    #         messages.add_message(self.request,
    #                              messages.ERROR,
    #                              "Cannot update. Seats have been booked for the show in this movie hall.")
    #         return HttpResponseRedirect(self.success_url)
    #     else:
    #         messages.add_message(self.request,
    #                              messages.SUCCESS,
    #                              "Movie hall has been updated successfully.")
    #         return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect(self.success_url)


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


class MovieShowDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('users:login')
    context_object_name = 'show'
    model = MovieShow
    http_method_names = ['get', 'post']
    template_name = 'movie_shows/shows/show_detail.html'
    extra_context = {'order_form': OrderCreateForm}

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
    http_method_names = ['get', 'post']
    template_name = 'movie_shows/shows/show_delete.html'

    def get_success_url(self):
        return reverse_lazy('shows:show_list')

    def form_valid(self, form):
        movie_show = self.get_object()

        if movie_show.sold_seats > 0:
            messages.add_message(self.request, messages.ERROR, "Cannot delete. Seats have been booked for this show")
            return HttpResponseForbidden("Cannot delete. Seats have been booked for this show.")

        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect('/cinema/shows/')


class OrderCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('users:login')
    model = Order
    form_class = OrderCreateForm
    http_method_names = ['get', 'post']
    template_name = 'movie_shows/orders/order_create.html'

    def get_success_url(self):
        movie_show = self.object.movie_show
        return movie_show.get_absolute_url()

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'movie_show_pk': self.kwargs['pk'],
            'customer': self.request.user})
        return kwargs

    def form_valid(self, form):
        order = form.save(commit=False)
        movie_show = MovieShow.objects.get(pk=form.movie_show_pk)
        movie_show.sold_seats += form.cleaned_data['seat_quantity']

        order.movie_show = movie_show

        order.seat_quantity = form.cleaned_data['seat_quantity']
        price = order.movie_show.ticket_price
        order.total_cost = order.seat_quantity * price

        customer = form.customer
        order.customer = customer
        customer.balance -= order.total_cost

        with transaction.atomic():
            order.save()
            customer.save()
            movie_show.save()

        messages.success(self.request, "Order successful!")
        return super().form_valid(form=form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid form data.")
        return HttpResponseRedirect(reverse_lazy('shows:show_list'))
