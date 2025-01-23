# backend/urls.py

"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from drf_yasg import views
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls.static import static
from backend import settings
from rest_framework.authtoken.views import obtain_auth_token

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
    path("admin/", admin.site.urls),
    path('api/', include([
            path('', include('core.urls')),
            path('', include('configuracion.urls')),
            # path('', include('turnos.urls')),
            path('', include('clientes.urls')),
            # path('', include('encuestas.urls')),
            path('', include('espera.urls')),
     ])),
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui",),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/token/", obtain_auth_token, name="api_token_auth"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
