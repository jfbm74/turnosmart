# configuracion/serializers.py

from rest_framework import serializers
from .models import Institucion, Imagen, Video, Audio, Ticket, Sistema, Voz

class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = ['id', 'nombre', 'siglas', 'direccion', 'ubicacion', 'telefono', 'email', 'sitio_web', 'mensaje']
        extra_kwargs = {
            'id': {'help_text': 'Identificador único de la Institución', 'read_only': True},
        }


class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = ['id', 'logo_pequeño', 'logo_grande', 'logo_ticket', 'footer', 'wallpaper_turnero']
        extra_kwargs = {
            'id': {'help_text': 'Identificador único de las imágenes', 'read_only': True},
        }


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'origen', 'url_video', 'video', 'estado']
        extra_kwargs = {
            'id': {'help_text': 'Identificador único del video', 'read_only': True},
        }

    def validate(self, data):
        if data['origen'] == 'URL' and not data.get('url_video'):
            raise serializers.ValidationError("Debe proporcionar una URL para el video.")
        if data['origen'] == 'SISTEMA' and not data.get('video'):
            raise serializers.ValidationError("Debe cargar un archivo de video.")
        return data


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ['id', 'timbre']
        extra_kwargs = {
            'id': {'help_text': 'Identificador único del audio', 'read_only': True},
        }


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'ancho_ticket', 'ancho_logo', 'alto_logo', 'logo_visible', 'fuente_turno', 'fuente_tramite', 
                  'tramite_visible', 'fuente_prioridad', 'prioridad_visible', 'fuente_nombre', 'nombre_visible', 
                  'fuente_espera', 'espera_visible', 'fuente_hora', 'hora_visible', 'fuente_fecha', 'fecha_visible', 
                  'fuente_sitio_web', 'sitio_web_visible', 'fuente_nombre_cliente', 'nombre_cliente_visible', 
                  'fuente_cedula_cliente', 'cedula_cliente_visible']
        extra_kwargs = {
            'id': {'help_text': 'Identificador único del ticket', 'read_only': True},
        }


class SistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sistema
        fields = ['id', 'tiempo_espera', 'umbral_espera', 'mostrar_turnos_anulados', 'mostrar_turnos_atendidos', 
                  'num_max_turnos_cedula', 'digitos_max_cedula_turnero', 'enviar_encuesta_cliente', 
                  'asignacion_automatica', 'version_sistema', 'copyright', 'contrasena_email_notificaciones', 
                  'puerto_notificaciones', 'duracion_link_recuperacion_clave', 'mostrar_turnos_llamados_sin_atender', 
                  'solicitar_confirmacion_obtener_turnos', 'abrir_encuesta_atencion', 'emision_ticket', 'url_copyright', 
                  'email_notificaciones', 'host_notificaciones', 'remitente_notificaciones', 
                  'enlace_recuperacion_clave', 'enlace_encuesta']
        extra_kwargs = {
            'id': {'help_text': 'Identificador único del sistema', 'read_only': True},
        }


class VozSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voz
        fields = ['id', 'llamado_turno_con_voz', 'origen_voz', 'idioma', 'tono', 'velocidad', 'volumen']
        extra_kwargs = {
            'id': {'help_text': 'Identificador único de la configuración de voz', 'read_only': True},
        }


class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = ['id', 'logo_pequeño', 'logo_grande', 'logo_ticket', 'footer', 'wallpaper_turnero']
        extra_kwargs = {
            'id': {'read_only': True, 'help_text': 'Identificador único de la imagen.'},
         }



class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'origen', 'url_video', 'video', 'estado']
        extra_kwargs = {
              'id': {'help_text': 'Identificador único del video', 'read_only': True},
              'origen': {'help_text': 'Define el origen del vídeo (URL o SISTEMA).'},
              'url_video': {'help_text': 'URL del video'},
              'video': {'help_text': 'Archivo del video en caso de ser cargado del sistema.'},
              'estado': {'help_text': 'Indica si el video está activo.'},
            }

    def validate(self, data):
        if data['origen'] == 'URL' and not data.get('url_video'):
            raise serializers.ValidationError("Debe proporcionar una URL para el video.")
        if data['origen'] == 'SISTEMA' and not data.get('video'):
            raise serializers.ValidationError("Debe cargar un archivo de video.")
        return data