# clientes/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.ClienteListCreateView.as_view(), name='clientes_list_create'),
    path('clientes/<int:pk>', views.ClienteDetailView.as_view(), name='clientes_detail')
]