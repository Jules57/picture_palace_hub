from django.urls import include, path
from rest_framework import routers

from movie_shows.api.resources import CinemaHallViewSet, MovieShowViewSet, MovieViewSet, OrderViewSet

router = routers.SimpleRouter()

router.register(r'halls', CinemaHallViewSet),
router.register(r'shows', MovieShowViewSet),
router.register(r'movies', MovieViewSet),
router.register(r'orders', OrderViewSet),

urlpatterns = [
    path('', include(router.urls)),
]
