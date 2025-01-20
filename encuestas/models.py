from django.db import models

# Create your models here.
class Encuesta(models.Model):
    """
    Modelo para las preguntas de encuestas.
    """
    pregunta = models.CharField(max_length=200)

    def __str__(self):
       return self.pregunta

class Respuesta(models.Model):
   """
    Modelo para las opciones de respuesta de las encuestas.
    """
   encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='respuestas')
   respuesta = models.CharField(max_length=200)

   def __str__(self):
        return self.respuesta
