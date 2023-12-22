from django.urls import include, path
from rest_framework import routers

from users.api.resources import LogoutApiView, CustomerViewSet, AuthToken

router = routers.SimpleRouter()

router.register(r'users', CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', AuthToken.as_view()),
    path('logout/', LogoutApiView.as_view())
]
