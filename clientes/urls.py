# clientes/urls.py

from django.urls import path
from . import views

# Las rutas ahora comienzan sin la `/`, ya que `/api/` se gestiona en backend/urls.py
urlpatterns = [
    path('clientes/', views.ClienteListCreateView.as_view(), name='clientes_list_create'),
    path('clientes/<int:pk>', views.ClienteDetailView.as_view(), name='clientes_detail')
]