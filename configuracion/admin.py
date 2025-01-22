from django.contrib import admin
from .models import Institucion, Imagen, Video, Audio, Ticket, Sistema, Voz

@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'siglas', 'direccion', 'email', 'telefono')
    search_fields = ('nombre', 'siglas', 'email')
    list_filter = ('nombre',)
    ordering = ('nombre',)


@admin.register(Imagen)
class ImagenAdmin(admin.ModelAdmin):
    list_display = ('id', 'logo_pequeño', 'logo_grande', 'logo_ticket', 'footer', 'wallpaper_turnero')
    ordering = ('id',)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'origen', 'url_video', 'video', 'estado')
    list_filter = ('estado', 'origen')
    search_fields = ('url_video',)
    ordering = ('id',)


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('id', 'timbre')
    ordering = ('id',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'ancho_ticket', 'logo_visible', 'tramite_visible', 'prioridad_visible')
    list_filter = ('logo_visible', 'tramite_visible', 'prioridad_visible')
    ordering = ('id',)


@admin.register(Sistema)
class SistemaAdmin(admin.ModelAdmin):
    list_display = ('id', 'version_sistema', 'email_notificaciones', 'host_notificaciones', 'emision_ticket')
    search_fields = ('version_sistema', 'email_notificaciones')
    ordering = ('id',)


@admin.register(Voz)
class VozAdmin(admin.ModelAdmin):
    list_display = ('id', 'llamado_turno_con_voz', 'origen_voz', 'idioma')
    list_filter = ('origen_voz',)
    ordering = ('id',)
