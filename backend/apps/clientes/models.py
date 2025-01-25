from django.db import models


# Create your models here.
class Cliente(models.Model):
    """
    Modelo para la información del cliente.
    """

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    documento = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
