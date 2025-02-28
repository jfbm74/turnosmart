from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    FranjaHorariaViewSet,
    HorarioViewSet,
    GenerarHorariosAPIView,
    HorariosListView,
    MenuListView,
    MenuViewSet,
    PrioridadListView,
    PrioridadViewSet,
    SalaViewSet,
    TurneroListView,
    TurneroViewSet,
)


# Registro de rutas con DefaultRouter
router = DefaultRouter()
router.register(r"franjas-horarias", FranjaHorariaViewSet, basename="franja-horaria")
router.register(r"horarios", HorarioViewSet, basename="horario")
router.register(r"turneros", TurneroViewSet, basename="turnero")
router.register(r"salas-espera", SalaViewSet, basename="sala-espera")
router.register(r"prioridades", PrioridadViewSet, basename="prioridad")
router.register(r"menus", MenuViewSet, basename="menus")

# Agregar rutas adicionales
urlpatterns = [
    path(
        "generar-horarios/", GenerarHorariosAPIView.as_view(), name="generar-horarios"
    ),
    path('turnos/prioridades/', PrioridadListView.as_view(), name='prioridades-list'),
    path("horarios/list/", HorariosListView.as_view(), name="horarios-list"),
    path('menu/list/', MenuListView.as_view(), name='menus-lista'),
    path('turnos/turneros/', TurneroListView.as_view(), name='turneros-list'),


] + router.urls