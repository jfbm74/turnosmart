from django.contrib import admin
from backend.apps.turnos.models import (
    FranjaHoraria,
    Horario,
    Sala,
    Menu,
    Prioridad,
    Turnero,
)


@admin.register(FranjaHoraria)
class FranjaHorariaAdmin(admin.ModelAdmin):
    """
    Configuración del modelo FranjaHoraria en el administrador.
    """
    list_display = ("hora_inicio", "hora_fin", "estado")
    list_filter = ("estado",)
    search_fields = ("hora_inicio", "hora_fin")


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Horario en el administrador.
    """
    list_display = (
        "franja_horaria",
        "lunes",
        "martes",
        "miercoles",
        "jueves",
        "viernes",
        "sabado",
        "domingo",
    )
    list_filter = ("lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo")
    search_fields = ("franja_horaria__hora_inicio", "franja_horaria__hora_fin")


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Sala en el administrador.
    """
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre", "descripcion")
    filter_horizontal = ("tramite_turnos_en_espera", "ventanillas_asignadas")


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Menu en el administrador.
    """
    list_display = ("nombre", "tipo", "horario_general", "tramite", "prioridad")
    list_filter = ("tipo", "horario_general")
    search_fields = ("nombre",)


@admin.register(Prioridad)
class PrioridadAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Prioridad en el administrador.
    """
    list_display = ("nombre", "prioridad")
    list_filter = ("prioridad",)
    search_fields = ("nombre",)


@admin.register(Turnero)
class TurneroAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Turnero en el administrador.
    """
    list_display = ("nombre", "ubicacion", "presentacion")
    list_filter = ("presentacion",)
    search_fields = ("nombre", "ubicacion")
    filter_horizontal = ("menus",)
