from django.db import models

# Create your models here.
class Institucion(models.Model):
    """
    Modelo para la información de la institución (configuración general).
    """
    nombre = models.CharField(max_length=200)
    siglas = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    ubicacion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    mensaje = models.TextField(blank=True, null=True)
    
    def __str__(self):
      return self.nombre
    


class Imagen(models.Model):
  """
  Modelo para las imágenes de la aplicación.
  """
  logo_pequeño = models.ImageField(upload_to='images/', blank=True, null=True)
  logo_grande = models.ImageField(upload_to='images/', blank=True, null=True)
  logo_ticket = models.ImageField(upload_to='images/', blank=True, null=True)
  footer = models.ImageField(upload_to='images/', blank=True, null=True)
  wallpaper_turnero = models.ImageField(upload_to='images/', blank=True, null=True)



class Video(models.Model):
    """
    Modelo para gestionar videos (URLs o archivos subidos).
    """
    origen = models.CharField(max_length=20, choices=[
        ('URL', 'URL Externa'),
        ('SISTEMA', 'Videos subidos en el sistema')
    ], default = 'URL')
    url_video = models.URLField(blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        if self.origen == 'URL':
          return self.url_video
        return f"Video id: {self.id}"


class Audio(models.Model):
    """
    Modelo para gestionar archivos de audio (timbre).
    """
    timbre = models.FileField(upload_to='audios/', blank=True, null=True)


class Ticket(models.Model):
  """
  Modelo para configurar los tickets.
  """
  ancho_ticket = models.IntegerField(default=80)
  ancho_logo = models.IntegerField(default=35)
  alto_logo = models.IntegerField(default=38)
  logo_visible = models.BooleanField(default=True)
  fuente_turno = models.IntegerField(default=14)
  fuente_tramite = models.IntegerField(default=5)
  tramite_visible = models.BooleanField(default=True)
  fuente_prioridad = models.IntegerField(default=3)
  prioridad_visible = models.BooleanField(default=True)
  fuente_nombre = models.IntegerField(default=2)
  nombre_visible = models.BooleanField(default=True)
  fuente_espera = models.IntegerField(default=3)
  espera_visible = models.BooleanField(default=True)
  fuente_hora = models.IntegerField(default=2)
  hora_visible = models.BooleanField(default=True)
  fuente_fecha = models.IntegerField(default=2)
  fecha_visible = models.BooleanField(default=True)
  fuente_sitio_web = models.IntegerField(default=1)
  sitio_web_visible = models.BooleanField(default=True)
  fuente_nombre_cliente = models.IntegerField(default=3)
  nombre_cliente_visible = models.BooleanField(default=True)
  fuente_cedula_cliente = models.IntegerField(default=3)
  cedula_cliente_visible = models.BooleanField(default=True)


class Sistema(models.Model):
    """
    Modelo para configurar el comportamiento general del sistema.
    """
    tiempo_espera = models.IntegerField(default=10)
    umbral_espera = models.IntegerField(default=5)
    mostrar_turnos_anulados = models.BooleanField(default=False)
    mostrar_turnos_atendidos = models.BooleanField(default=False)
    num_max_turnos_cedula = models.IntegerField(default=1)
    digitos_max_cedula_turnero = models.IntegerField(default=15)
    enviar_encuesta_cliente = models.BooleanField(default=False)
    asignacion_automatica = models.BooleanField(default=False)
    version_sistema = models.CharField(max_length=20, default='4.0.1')
    copyright = models.CharField(max_length=200, default='jairo blanquiceth')
    contrasena_email_notificaciones = models.CharField(max_length=200, default='a', blank=True, null=True)
    puerto_notificaciones = models.IntegerField(default=587, blank=True, null=True)
    duracion_link_recuperacion_clave = models.IntegerField(default=1)
    mostrar_turnos_llamados_sin_atender = models.BooleanField(default=True)
    solicitar_confirmacion_obtener_turnos = models.BooleanField(default=False)
    abrir_encuesta_atencion = models.BooleanField(default=False)
    emision_ticket = models.CharField(max_length=20, choices=[
        ('IMPRIMIR', 'Imprimir'),
         ('QR', 'QR'),
    ], default = 'IMPRIMIR')
    url_copyright = models.URLField(default='https://piisa.com', blank=True, null=True)
    email_notificaciones = models.EmailField(default='jairoblanquicethcuello@gmail.com', blank=True, null=True)
    host_notificaciones = models.CharField(max_length=200, default='smtp.gmail.com', blank=True, null=True)
    remitente_notificaciones = models.CharField(max_length=200, default='Socioturnos', blank=True, null=True)
    enlace_recuperacion_clave = models.URLField(default='http://socioturnos.com/digiturnos/recuperarclave.php', blank=True, null=True)
    enlace_encuesta = models.URLField(default='http://socioturnos.com/digiturnos/encuesta.php', blank=True, null=True)


class Voz(models.Model):
   """
   Modelo para la configuracion de voz del sistema.
   """
   llamado_turno_con_voz = models.BooleanField(default=True)
   origen_voz = models.CharField(max_length=20, choices=[
        ('TTS NAVEGADOR WEB', 'TTS NAVEGADOR WEB'),
       ('URL EXTERNA', 'URL Externa')
   ], default = 'TTS NAVEGADOR WEB')
   idioma = models.CharField(max_length=200, default='ESPAÑOL (ESPAÑA)')
   tono = models.FloatField(default=1.0)
   velocidad = models.FloatField(default=1.0)
   volumen = models.FloatField(default=1.0)






