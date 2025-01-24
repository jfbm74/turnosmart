from django.urls import include, path
from .views import (
    GrupoViewSet,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    UserRegister,
    UserLogin,
    UserProfileView,
    UserLogoutView,
    UserCreateView,
    VentanillaViewSet,
)
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'grupos', GrupoViewSet, basename='grupos')
router.register(r'ventanillas', VentanillaViewSet, basename='ventanilla')

urlpatterns = [
    path("auth/register", UserRegister.as_view(), name="register"),
    path("auth/login", UserLogin.as_view(), name="login"),
    path("auth/profile", UserProfileView.as_view(), name="profile"),
    path("auth/logout", UserLogoutView.as_view(), name="logout"),
    path("users", UserCreateView.as_view(), name="create_user"),  
    path("auth/password-change", PasswordChangeView.as_view(), name="password_change"),
    path("auth/password-reset-request", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("auth/password-reset-confirm", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('', include(router.urls)),
]