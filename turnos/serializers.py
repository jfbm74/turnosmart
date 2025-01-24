from rest_framework import serializers
from .models import FranjaHoraria, Horario

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