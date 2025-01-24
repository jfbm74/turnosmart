from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FranjaHorariaViewSet, HorarioViewSet, GenerarHorariosAPIView

# Registro de rutas con DefaultRouter
router = DefaultRouter()
router.register(r'franjas-horarias', FranjaHorariaViewSet, basename='franja-horaria')
router.register(r'horarios', HorarioViewSet, basename='horario')

# Agregar rutas adicionales
urlpatterns = router.urls + [
    path('generar-horarios/', GenerarHorariosAPIView.as_view(), name='generar-horarios'),
]
