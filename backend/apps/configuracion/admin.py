from django.contrib import admin
from backend.apps.configuracion.models import (
    Institucion,
    Imagen,
    Video,
    Audio,
    Ticket,
    Sistema,
    Voz,
)


@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "siglas", "direccion", "telefono", "email")
    search_fields = ("nombre", "siglas", "direccion", "telefono", "email")


@admin.register(Imagen)
class ImagenAdmin(admin.ModelAdmin):
    list_display = ("logo_pequeño", "logo_grande", "logo_ticket", "footer", "wallpaper_turnero")


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("origen", "url_video", "video", "estado")
    list_filter = ("origen", "estado")
    search_fields = ("url_video",)


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ("timbre",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("ancho_ticket", "logo_visible", "fuente_turno", "tramite_visible")
    list_filter = ("logo_visible", "tramite_visible")


@admin.register(Sistema)
class SistemaAdmin(admin.ModelAdmin):
    list_display = ("version_sistema", "tiempo_espera", "mostrar_turnos_anulados", "enviar_encuesta_cliente")
    list_filter = ("mostrar_turnos_anulados", "enviar_encuesta_cliente")
    search_fields = ("version_sistema", "copyright")


@admin.register(Voz)
class VozAdmin(admin.ModelAdmin):
    list_display = ("llamado_turno_con_voz", "origen_voz", "idioma", "tono", "velocidad", "volumen")
    list_filter = ("llamado_turno_con_voz", "origen_voz")
