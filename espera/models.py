from django.db import models

from turnos.models import Sala


# Create your models here.
class Espera(models.Model):
    """
    Modelo para configurar los mensajes de la sala de espera.
    """

    etiquetas_llamado_individual_multiple = models.TextField(
        default="""{turno}: Número de turno completo.
        {turno_dividido}: Número de turno deletreado.
        {cedula}: Número de cédula completa (En caso de que la cédula haya sido ingresada).
        {cliente_nombre}: Nombre cliente (En caso de que al momento de llamar el turno el cliente haya ingresado su cédula).
        {cliente_apellido}: Apellido Cliente (En caso de que al momento de llamar el turno el cliente haya ingresado su cédula).
        {cedula_dividido}:Número de cédula deletreada (En caso de que la cédula haya sido ingresada).
        {cedula_existe_inicio} {cedula_existe_cierre}: Mensaje condicional (En caso de que la cédula haya sido ingresada).
        {turno}: Número de turno entero.
        {ventanilla}: Nombre de la ventanilla.""",
        blank=True,
        null=True,
    )
    llamado_sala_espera_individual = models.CharField(
        max_length=300,
        default="@ turno. {turno_dividido} {cedula_existe_inicio} con documento {cedula_existe_cierre} {cedula} pase a. {ventanilla}",
        blank=True,
        null=True,
    )
    llamado_sala_espera_multiple_parte1 = models.CharField(
        max_length=300, default="@ Turnos.", blank=True, null=True
    )
    llamado_sala_espera_multiple_parte2 = models.CharField(
        max_length=300, default="@ {turno_dividido}", blank=True, null=True
    )
    llamado_sala_espera_multiple_parte3 = models.CharField(
        max_length=300, default="@ pasen a. {ventanilla}", blank=True, null=True
    )
    titulo_columna_turnos = models.CharField(
        max_length=50, default="TURNO", blank=True, null=True
    )
    titulo_columna_espera = models.CharField(
        max_length=50, default="ESPERA TR", blank=True, null=True
    )
    titulo_columna_ventanillas = models.CharField(
        max_length=50, default="SERVICIO", blank=True, null=True
    )
    limite_turnos_visibles_presentacion = models.IntegerField(
        default=7, blank=True, null=True
    )


class ColaEspera(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name="colas")
    max_turnos = models.IntegerField(default=10)
    ordenar_por = models.CharField(
        max_length=20,
        choices=[("tiempo", "Tiempo de Espera"), ("prioridad", "Prioridad")],
        default="tiempo",
    )
    mostrar_atendidos = models.BooleanField(default=True)
    mostrar_anulados = models.BooleanField(default=False)
    limite_turnos_visibles_presentacion = models.IntegerField(
        default=7, blank=True, null=True
    )

    def __str__(self):
        return f"Cola de {self.sala.nombre}"
