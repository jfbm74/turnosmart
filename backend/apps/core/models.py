from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserProfile(AbstractUser):
    cedula = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    foto = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    ventanillas_atencion = models.ManyToManyField(
        "Ventanilla", blank=True, related_name="usuarios"
    )
    perfil = models.ForeignKey(
        "Perfil",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuarios",
    )
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="userprofile_groups",  # Agrega este related_name
        related_query_name="userprofile",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="userprofile_permissions",  # Agrega este related_name
        related_query_name="userprofile",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Perfil(models.Model):
    """
    Modelo para definir los perfiles (roles) de usuario y su tipo de atención.
    """

    nombre = models.CharField(max_length=100)
    acronimo = models.CharField(max_length=20)
    tipo_seleccion = models.CharField(
        max_length=20,
        choices=[
            ("MANUAL", "Manual"),
            ("AUTOMATICA", "Automática"),
            ("SISTEMA", "Sistema"),
        ],
        default="SISTEMA",
    )

    def __str__(self):
        return self.nombre


from django.db import models


class Opcion(models.Model):
    """
    Modelo para definir las opciones del menú lateral y su configuración.
    """

    nombre = models.CharField(max_length=100)
    acronimo = models.CharField(max_length=20)
    icono = models.CharField(max_length=100)
    vista = models.CharField(max_length=200)
    perfiles = models.ManyToManyField("Perfil", blank=True, related_name="opciones")

    def __str__(self):
        return self.nombre


class Ventanilla(models.Model):
    """
    Modelo para definir los puntos de atención.
    """

    id_ventanilla = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id_ventanilla} - {self.descripcion}"


class Tramite(models.Model):
    """
    Modelo para los trámites de la aplicación.
    """

    nombre = models.CharField(max_length=100)
    iniciales = models.CharField(max_length=20)
    cliente_requerido = models.CharField(
        max_length=50,
        choices=[
            ("no", "Información de cliente no requerida"),
            ("atender", "Información de cliente requerida al ser atendido"),
            ("turno", "Información de cliente(Cédula) requerida al tomar turno"),
        ],
        default="no",
    )
    ventanilla_atencion = models.ForeignKey(
        "core.Ventanilla",
        on_delete=models.SET_NULL,
        null=True,
        related_name="tramites_atencion",
    )
    ventanilla_transferencia_frecuente = models.ManyToManyField(
        "core.Ventanilla", blank=True, related_name="tramites_transferencia_frecuente"
    )
    grupo_transferencia_frecuente = models.ManyToManyField(
        "core.Grupo", blank=True, related_name="tramites_grupo_transferencia_frecuente"
    )

    def __str__(self):
        return self.nombre


class Grupo(models.Model):
    """
    Modelo para definir grupos de ventanillas de atención.
    """

    nombre = models.CharField(max_length=100)
    ventanillas_atencion = models.ManyToManyField(
        "core.Ventanilla", related_name="grupos"
    )
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
