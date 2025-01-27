from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    ImagenListView,
    InstitucionViewSet,
    ImagenViewSet,
    VideoViewSet,
    AudioViewSet,
    TicketViewSet,
    SistemaViewSet,
    VozViewSet,
    InstitucionListView,  # Importar la vista de plantilla
)



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
] + router.urls
