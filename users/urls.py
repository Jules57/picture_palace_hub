from django.urls import path

from users.views import RegisterView, Login, Logout, CustomerDetailView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/<int:pk>/', CustomerDetailView.as_view(), name='profile'),
]
