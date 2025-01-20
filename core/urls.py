from django.urls import path
from .views import UserRegister, UserLogin, UserProfileView, UserLogoutView

urlpatterns = [
     path('auth/register', UserRegister.as_view(), name='register'),
     path('auth/login', UserLogin.as_view(), name='login'),
     path('auth/profile', UserProfileView.as_view(), name='profile'),
     path('auth/logout', UserLogoutView.as_view(), name='logout'),
]