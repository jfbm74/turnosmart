from rest_framework import serializers
from .models import FranjaHoraria, Horario, Turnero

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