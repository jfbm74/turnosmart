from rest_framework import serializers
from .models import FranjaHoraria, Horario, Prioridad, Turnero, Menu, Sala


class FranjaHorariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FranjaHoraria
        fields = ["id", "hora_inicio", "hora_fin", "estado"]


class HorarioSerializer(serializers.ModelSerializer):
    franja_horaria = serializers.PrimaryKeyRelatedField(
        queryset=FranjaHoraria.objects.all()
    )

    class Meta:
        model = Horario
        fields = [
            "id",
            "franja_horaria",
            "lunes",
            "martes",
            "miercoles",
            "jueves",
            "viernes",
            "sabado",
            "domingo",
        ]




class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "nombre", "tipo", "horario_general", "tramite", "prioridad", "imagen", "descripcion"] # Added field here
        # add validations
        extra_kwargs = {
            'id': {'read_only': True, 'help_text': 'The unique identifier for the menu.'},
            'nombre': {'required': True, 'help_text': 'The name of the menu.'},
            'tipo': {'required': True, 'help_text': 'The type of menu (CONTENEDOR or TRAMITE).'},
            'horario_general': {'help_text': 'Whether the menu uses the general schedule.'},
            'tramite': {'required': False, 'allow_null': True, 'help_text': 'The associated Tramite (if applicable).'},
            'prioridad': {'required': False, 'allow_null': True, 'help_text': 'The associated Prioridad (if applicable).'},
            'imagen': {'required': False, 'help_text': 'The URL or path to the menu image.'},
            'descripcion': {'help_text': 'A description of the menu.'},
        }


class TurneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turnero
        fields = ['id', 'nombre', 'ubicacion', 'presentacion', 'menus']
        extra_kwargs = {
            'id': {'read_only': True},
            'menus': {'required': False}
        }

    def create(self, validated_data):
        menus_data = validated_data.pop('menus', [])
        turnero = Turnero.objects.create(**validated_data)
        if menus_data:
            turnero.menus.set(menus_data)
        return turnero

    def update(self, instance, validated_data):
        menus_data = validated_data.pop('menus', [])
        instance = super().update(instance, validated_data)
        if 'menus' in self.initial_data:
            instance.menus.set(menus_data)
        return instance

    class Meta:
        model = Turnero
        fields = ['id', 'nombre', 'ubicacion', 'presentacion', 'menus']


class TurneroMenuAssociationSerializer(serializers.Serializer):
    menu_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="Lista de IDs de los menús a asociar con el turnero.",
    )


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ["id", "nombre", "descripcion"]

    def validate_nombre(self, value):
        """
        Validate that the name is not empty and has a reasonable length.
        """
        if not value:
            raise serializers.ValidationError(
                "El nombre de la sala no puede estar vacío."
            )
        if len(value) < 3:
            raise serializers.ValidationError(
                "El nombre de la sala debe tener al menos 3 caracteres."
            )
        if len(value) > 100:
            raise serializers.ValidationError(
                "El nombre de la sala no puede exceder 100 caracteres."
            )
        return value


class PrioridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prioridad
        fields = ['id', 'nombre', 'prioridad']
        extra_kwargs = {
              'id': {'help_text': 'Identificador único de la prioridad', 'read_only': True},
              'nombre': {'help_text': 'Nombre de la prioridad'},
            'prioridad': {'help_text': 'Nivel de prioridad de los turnos'}
        }
