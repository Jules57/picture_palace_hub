from django.urls import path, include

from users.views import RegisterView, Login, Logout, CustomerDetailView

app_name = 'users'

urlpatterns = [
    path('api/', include('users.api.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/<int:pk>/', CustomerDetailView.as_view(), name='profile'),
]
