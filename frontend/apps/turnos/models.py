from django.db import models


# Create your models here.
class FranjaHoraria(models.Model):
    """
    Modelo para definir franjas horarias (rangos de tiempo).
    """

    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hora_inicio} - {self.hora_fin}"


class Horario(models.Model):
    """
    Modelo para asociar franjas horarias a días de la semana.
    """
    franja_horaria = models.ForeignKey(FranjaHoraria, on_delete=models.CASCADE)
    lunes = models.BooleanField(default=False)
    martes = models.BooleanField(default=False)
    miercoles = models.BooleanField(default=False)
    jueves = models.BooleanField(default=False)
    viernes = models.BooleanField(default=False)
    sabado = models.BooleanField(default=False)
    domingo = models.BooleanField(default=False)

    def get_estado_dia(self, dia):
        """
        Retorna el estado real del día teniendo en cuenta el estado de la franja horaria
        """
        dia_activo = getattr(self, dia)
        return dia_activo and self.franja_horaria.estado

    @property
    def estado_lunes(self):
        return self.get_estado_dia('lunes')
    
    @property
    def estado_martes(self):
        return self.get_estado_dia('martes')
    
    @property
    def estado_miercoles(self):
        return self.get_estado_dia('miercoles')
    
    @property
    def estado_jueves(self):
        return self.get_estado_dia('jueves')
    
    @property
    def estado_viernes(self):
        return self.get_estado_dia('viernes')
    
    @property
    def estado_sabado(self):
        return self.get_estado_dia('sabado')
    
    @property
    def estado_domingo(self):
        return self.get_estado_dia('domingo')

    def __str__(self):
        return str(self.franja_horaria)
    



class Sala(models.Model):
    """
    Modelo para la gestión de las salas de espera.
    """

    nombre = models.CharField(max_length=100)
    tramite_turnos_en_espera = models.ManyToManyField(
        "core.Tramite", related_name="salas_espera"
    )
    ventanillas_asignadas = models.ManyToManyField(
        "core.Ventanilla", related_name="salas_atencion"
    )
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Menu(models.Model):
    """
    Modelo para la gestión de los menús de los turneros.
    """

    TIPO_MENU = [
        ("CONTENEDOR", "Menú Contenedor"),
        ("TRAMITE", "Trámite"),
    ]
    nombre = models.CharField(max_length=200, blank=True, null=True)
    tipo = models.CharField(max_length=100, choices=TIPO_MENU)
    horario_general = models.BooleanField(default=True)
    tramite = models.ForeignKey(
        "core.Tramite", on_delete=models.SET_NULL, blank=True, null=True
    )
    prioridad = models.ForeignKey(
        "Prioridad", on_delete=models.SET_NULL, blank=True, null=True
    )
    imagen = models.ImageField(upload_to="menu_icons/", blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Prioridad(models.Model):
    """
    Modelo para definir las prioridades.
    """

    nombre = models.CharField(max_length=100)
    prioridad = models.CharField(
        max_length=20,
        choices=[
            ("ALTA", "ALTA"),
            ("MEDIA", "MEDIA"),
            ("BAJA", "BAJA"),
            ("MUY ALTA", "MUY ALTA"),
        ],
        default="MEDIA",
    )

    def __str__(self):
        return self.nombre


class Turnero(models.Model):
    """
    Modelo para la gestión de los turneros.
    """

    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200, blank=True, null=True)
    menus = models.ManyToManyField(Menu, related_name="turneros", blank=True)
    presentacion = models.CharField(
        max_length=10,
        choices=[
            ("IMPRIMIR", "Imprimir"),
            ("QR", "QR"),
        ],
        default="IMPRIMIR",
    )

    def __str__(self):
        return self.nombre
