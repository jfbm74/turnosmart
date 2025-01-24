from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FranjaHorariaViewSet, HorarioViewSet, GenerarHorariosAPIView, TurneroViewSet

# Registro de rutas con DefaultRouter
router = DefaultRouter()
router.register(r'franjas-horarias', FranjaHorariaViewSet, basename='franja-horaria')
router.register(r'horarios', HorarioViewSet, basename='horario')
router.register(r'turneros', TurneroViewSet, basename='turnero')

# Agregar rutas adicionales
urlpatterns = router.urls + [
    path('generar-horarios/', GenerarHorariosAPIView.as_view(), name='generar-horarios'),
]
