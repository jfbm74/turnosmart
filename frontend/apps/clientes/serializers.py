# clientes/serializers.py

from rest_framework import serializers
from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            "id",
            "nombre",
            "apellido",
            "documento",
            "email",
            "direccion",
            "telefono",
            "estado",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "documento": {
                "required": True,
                "help_text": "Número de documento de identidad del cliente.",
            },
            "nombre": {"required": True, "help_text": "Nombre del cliente"},
            "apellido": {"help_text": "Apellido del cliente"},
            "email": {"help_text": "Correo electrónico del cliente."},
            "direccion": {"help_text": "Dirección del cliente."},
            "telefono": {"help_text": "Teléfono del cliente."},
            "estado": {"help_text": "Estado del cliente."},
        }


class ClienteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "nombre", "apellido", "documento", "email", "estado"]
