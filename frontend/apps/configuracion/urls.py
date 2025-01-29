from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (
    ImagenListView,
    InstitucionViewSet,
    ImagenViewSet,
    SistemaListView,
    TicketListView,
    TicketPreviewView,
    VideoViewSet,
    AudioViewSet,
    TicketViewSet,
    SistemaViewSet,
    VozViewSet,
    InstitucionListView,
    VideoListView,
    AudioListView,
    TicketListView,
)
from . import views




# Configurar el enrutador
router = DefaultRouter()
router.register(r'instituciones', InstitucionViewSet, basename='institucion')
router.register(r'imagenes', ImagenViewSet, basename='imagen')
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'audios', AudioViewSet, basename='audio')
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'sistemas', SistemaViewSet, basename='sistema')
router.register(r'voces', VozViewSet, basename='voz')

# Agregar la URL de la vista de plantilla antes de las URLs generadas por el enrutador
urlpatterns = [
    path('configuracion/instituciones/', InstitucionListView.as_view(), name='instituciones-lista'),
    path('configuracion/imagenes/', ImagenListView.as_view(), name='imagenes-lista'),
    path('configuracion/videos/', VideoListView.as_view(), name='videos-lista'),
    path('configuracion/audios/', AudioListView.as_view(), name='audios-lista'),
    path('configuracion/tickets/', TicketListView.as_view(), name='tickets-lista'),
    path('configuracion/tickets/preview/<int:pk>/', TicketPreviewView.as_view(), name='ticket-preview'),
    path('ticket-preview/<int:pk>/', TicketPreviewView.as_view(), name='ticket-preview'),
    path('configuracion/sistemas/', SistemaListView.as_view(), name='sistemas-lista'), #add this url
] + router.urls