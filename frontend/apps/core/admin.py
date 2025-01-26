from django.contrib import admin
from apps.core.models import (
    UserProfile,
    Perfil,
    Opcion,
    Ventanilla,
    Tramite,
    Grupo,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Configuración del modelo UserProfile en el administrador.
    """
    list_display = ("username", "first_name", "last_name", "email", "perfil", "cedula")
    search_fields = ("username", "first_name", "last_name", "email", "cedula")
    list_filter = ("perfil",)
    filter_horizontal = ("ventanillas_atencion", "groups", "user_permissions")


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Perfil en el administrador.
    """
    list_display = ("nombre", "acronimo", "tipo_seleccion")
    list_filter = ("tipo_seleccion",)
    search_fields = ("nombre", "acronimo")


@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Opcion en el administrador.
    """
    list_display = ("nombre", "acronimo", "icono", "vista")
    search_fields = ("nombre", "acronimo", "vista")


@admin.register(Ventanilla)
class VentanillaAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Ventanilla en el administrador.
    """
    list_display = ("id_ventanilla", "descripcion", "estado")
    list_filter = ("estado",)
    search_fields = ("descripcion",)


@admin.register(Tramite)
class TramiteAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Tramite en el administrador.
    """
    list_display = ("nombre", "iniciales", "cliente_requerido", "ventanilla_atencion")
    list_filter = ("cliente_requerido",)
    search_fields = ("nombre", "iniciales")
    filter_horizontal = ("ventanilla_transferencia_frecuente", "grupo_transferencia_frecuente")


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Grupo en el administrador.
    """
    list_display = ("nombre", "estado")
    list_filter = ("estado",)
    search_fields = ("nombre",)
    filter_horizontal = ("ventanillas_atencion",)
