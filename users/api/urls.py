from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken

from users.api.resources import LogoutApiView, CustomerViewSet

router = routers.SimpleRouter()

router.register(r'users', CustomerViewSet)

# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('login/', ObtainAuthToken.as_view()),
    path('logout/', LogoutApiView.as_view())
]
