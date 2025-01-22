from rest_framework.routers import DefaultRouter
from .views import (
    InstitucionViewSet,
    ImagenViewSet,
    VideoViewSet,
    AudioViewSet,
    TicketViewSet,
    SistemaViewSet,
    VozViewSet,
)

router = DefaultRouter()
router.register(r'instituciones', InstitucionViewSet, basename='institucion')
router.register(r'imagenes', ImagenViewSet, basename='imagen')
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'audios', AudioViewSet, basename='audio')
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'sistemas', SistemaViewSet, basename='sistema')
router.register(r'voces', VozViewSet, basename='voz')

urlpatterns = router.urls
