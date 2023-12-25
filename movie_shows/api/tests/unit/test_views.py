from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from movie_shows.models import CinemaHall
from movie_shows.api.resources import CinemaHallViewSet
from movie_shows.api.serializers import CinemaHallReadSerializer, CinemaHallWriteSerializer
from users.models import Customer


class CinemaHallViewSetTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin_user = Customer.objects.create(username='admin', is_staff=True, is_superuser=True)
        self.non_admin_user = Customer.objects.create(username='user', is_staff=False, is_superuser=False)
        self.cinema_hall = CinemaHall.objects.create(
                name='Test Hall',
                seats=50,
                screen_size='Standard',
                screen_type='2D',
        )

    def test_get_serializer_class_read_method(self):
        view = CinemaHallViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/halls/')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_serializer_class_invalid_write_method(self):
        view = CinemaHallViewSet.as_view({'post': 'create'})
        request = self.factory.post('/api/cinema-halls/', {'name': 'Invalid Hall'})
        force_authenticate(request, user=self.non_admin_user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
