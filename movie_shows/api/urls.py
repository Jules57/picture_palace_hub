from django.urls import include, path
from rest_framework import routers

from movie_shows.api.resources import CinemaHallViewSet, MovieShowViewSet, MovieViewSet

router = routers.SimpleRouter()

router.register(r'halls', CinemaHallViewSet),
router.register(r'shows', MovieShowViewSet),
router.register(r'movies', MovieViewSet),

urlpatterns = [
    path('', include(router.urls)),
]
