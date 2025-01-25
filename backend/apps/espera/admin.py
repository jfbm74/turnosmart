from django.contrib import admin
from backend.apps.espera.models import Espera, ColaEspera


@admin.register(Espera)
class EsperaAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Espera en el administrador.
    """
    list_display = (
        "llamado_sala_espera_individual",
        "titulo_columna_turnos",
        "titulo_columna_espera",
        "titulo_columna_ventanillas",
        "limite_turnos_visibles_presentacion",
    )
    search_fields = ("titulo_columna_turnos", "titulo_columna_espera", "titulo_columna_ventanillas")


@admin.register(ColaEspera)
class ColaEsperaAdmin(admin.ModelAdmin):
    """
    Configuración del modelo ColaEspera en el administrador.
    """
    list_display = (
        "sala",
        "max_turnos",
        "ordenar_por",
        "mostrar_atendidos",
        "mostrar_anulados",
        "limite_turnos_visibles_presentacion",
    )
    list_filter = ("ordenar_por", "mostrar_atendidos", "mostrar_anulados")
    search_fields = ("sala__nombre",)
