from django.urls import path
from .views import UserRegister, UserLogin, UserProfileView, UserLogoutView, UserCreateView

urlpatterns = [
     path('auth/register', UserRegister.as_view(), name='register'),
     path('auth/login', UserLogin.as_view(), name='login'),
     path('auth/profile', UserProfileView.as_view(), name='profile'),
     path('auth/logout', UserLogoutView.as_view(), name='logout'),
     path('users', UserCreateView.as_view(), name='create_user'), # Agrega el nombre a este endpoint
]