"""velzon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.decorators import login_required
from .views import MyPasswordChangeView, MyPasswordSetView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg import views
from drf_yasg import openapi
from rest_framework import permissions


schema_view = views.get_schema_view(
    openapi.Info(
        title="TurnoSmart API",
        default_version="v1",
        description="Documentación de la API REST para el sistema TurnoSmart",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="pipebustamante@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        "api/",
        include(
            [
                path("", include("apps.core.urls")),
                path("", include("apps.configuracion.urls")),
                path("", include("apps.turnos.urls")),
                path("", include("apps.clientes.urls")),
                # path('', include('backend.apps.encuestas.urls')),
                path("", include("apps.espera.urls")),
            ]
        ),
    ),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/token/", obtain_auth_token, name="api_token_auth"),

    # Dashboard
    path('',include('dashboards.urls')),

    # Layouts
    path('layouts/',include('layouts.urls')),

    # Pages
    path('pages/',include('pages.urls')),
    path(
        "account/password/change/",
        login_required(MyPasswordChangeView.as_view()),
        name="account_change_password",
    ),
    path(
        "account/password/set/",
        login_required(MyPasswordSetView.as_view()),
        name="account_set_password",
    ),
    # All Auth 
    path('account/', include('allauth.urls')),

    # Clientes (apps/clientes/urls.py)
    path('api/', include('apps.clientes.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)