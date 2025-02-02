from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    FranjaHorariaViewSet,
    HorarioViewSet,
    GenerarHorariosAPIView,
    PrioridadListView,
    PrioridadViewSet,
    SalaViewSet,
    TurneroViewSet,
)

# Registro de rutas con DefaultRouter
router = DefaultRouter()
router.register(r"franjas-horarias", FranjaHorariaViewSet, basename="franja-horaria")
router.register(r"horarios", HorarioViewSet, basename="horario")
router.register(r"turneros", TurneroViewSet, basename="turnero")
router.register(r"salas-espera", SalaViewSet, basename="sala-espera")
router.register(r"prioridades", PrioridadViewSet, basename="prioridad")

# Agregar rutas adicionales
urlpatterns = [
    path(
        "generar-horarios/", GenerarHorariosAPIView.as_view(), name="generar-horarios"
    ),
    path('turnos/prioridades/', PrioridadListView.as_view(), name='prioridades-list'),
] + router.urls