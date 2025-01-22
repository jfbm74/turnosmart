from django.urls import path
from .views import (
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    UserRegister,
    UserLogin,
    UserProfileView,
    UserLogoutView,
    UserCreateView,
)

# Las rutas ahora comienzan sin la `/`, ya que `/api/` se gestiona en backend/urls.py
urlpatterns = [
    path("auth/register", UserRegister.as_view(), name="register"),
    path("auth/login", UserLogin.as_view(), name="login"),
    path("auth/profile", UserProfileView.as_view(), name="profile"),
    path("auth/logout", UserLogoutView.as_view(), name="logout"),
    path(
        "users", UserCreateView.as_view(), name="create_user"
    ),  # Agrega el nombre a este endpoint
    path("auth/password-change", PasswordChangeView.as_view(), name="password_change"),
    path(
        "auth/password-reset-request",
        PasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
    path(
        "auth/password-reset-confirm",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]