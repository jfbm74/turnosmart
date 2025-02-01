# apps/clientes/urls.py

from django.urls import path
from .views import ClienteListCreateView, ClienteDetailView, clientes_list_view

urlpatterns = [
    # API Endpoints
    path("clientes/", ClienteListCreateView.as_view(), name="clientes_list_create"),
    path("clientes/<int:pk>/", ClienteDetailView.as_view(), name="clientes_detail"),
    
    # Vista para renderizar HTML
    path("clientes/lista/", clientes_list_view, name="clientes-lista"),
]
