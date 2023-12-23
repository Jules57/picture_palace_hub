from django.urls import include, path
from rest_framework import routers

from users.api.resources import LogoutApiView, CustomerViewSet, CustomAuthTokenLogin

router = routers.SimpleRouter()

router.register(r'users', CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthTokenLogin.as_view()),
    path('logout/', LogoutApiView.as_view())
]
