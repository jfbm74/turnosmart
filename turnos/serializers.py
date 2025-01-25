from rest_framework import serializers
from .models import FranjaHoraria, Horario, Turnero, Menu, Sala


class FranjaHorariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FranjaHoraria
        fields = ['id', 'hora_inicio', 'hora_fin', 'estado']


class HorarioSerializer(serializers.ModelSerializer):
    franja_horaria = serializers.PrimaryKeyRelatedField(queryset=FranjaHoraria.objects.all())

    class Meta:
        model = Horario
        fields = [
            'id', 'franja_horaria', 'lunes', 'martes', 'miercoles', 
            'jueves', 'viernes', 'sabado', 'domingo'
        ]

class TurneroSerializer(serializers.ModelSerializer):
  class Meta:
        model = Turnero
        fields = ['id', 'nombre', 'presentacion']
        extra_kwargs = {
            'id': {'read_only': True, 'help_text': 'Identificador único del turnero.'},
            'nombre': {'help_text': 'Nombre del turnero'},
            'presentacion': {'help_text': 'Tipo de presentación del turno (IMPRIMIR o QR).'},
         }


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'nombre', 'descripcion']


class TurneroSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(many=True, read_only=True)

    class Meta:
        model = Turnero
        fields = ['id', 'nombre', 'ubicacion', 'menus']


class TurneroMenuAssociationSerializer(serializers.Serializer):
    menu_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="Lista de IDs de los menús a asociar con el turnero."
    )


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['id', 'nombre', 'descripcion']
        
    def validate_nombre(self, value):
        """
        Validate that the name is not empty and has a reasonable length.
        """
        if not value:
            raise serializers.ValidationError("El nombre de la sala no puede estar vacío.")
        if len(value) < 3:
            raise serializers.ValidationError("El nombre de la sala debe tener al menos 3 caracteres.")
        if len(value) > 100:
            raise serializers.ValidationError("El nombre de la sala no puede exceder 100 caracteres.")
        return value