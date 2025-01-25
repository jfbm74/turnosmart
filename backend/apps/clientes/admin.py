from django.contrib import admin
from backend.apps.clientes.models import Cliente
# Register your models here.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Cliente en el administrador.
    """
    list_display = ("nombre", "apellido", "documento", "email", "telefono", "estado")
    list_filter = ("estado",)
    search_fields = ("nombre", "apellido", "documento", "email")