from rest_framework import serializers
from .models import ColaEspera, Espera

class EsperaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espera
        fields = ['id', 'etiquetas_llamado_individual_multiple', 'llamado_sala_espera_individual', 'llamado_sala_espera_multiple_parte1',
                'llamado_sala_espera_multiple_parte2', 'llamado_sala_espera_multiple_parte3', 'titulo_columna_turnos',
                'titulo_columna_espera', 'titulo_columna_ventanillas', 'limite_turnos_visibles_presentacion']
    extra_kwargs = {
        'id': {'read_only': True, 'help_text': 'Identificador único de la configuración de espera.'},
        'etiquetas_llamado_individual_multiple': {'help_text': 'Etiquetas para la construcción de mensajes.'},
        'llamado_sala_espera_individual': {'help_text': 'Mensaje para llamado individual en sala de espera.'},
        'llamado_sala_espera_multiple_parte1': {'help_text': 'Primera parte del mensaje para llamado múltiple en sala de espera.'},
        'llamado_sala_espera_multiple_parte2': {'help_text': 'Segunda parte del mensaje para llamado múltiple en sala de espera.'},
        'llamado_sala_espera_multiple_parte3': {'help_text': 'Tercera parte del mensaje para llamado múltiple en sala de espera.'},
        'titulo_columna_turnos': {'help_text': 'Título de la columna de turnos en la presentación.'},
        'titulo_columna_espera': {'help_text': 'Título de la columna de espera en la presentación.'},
        'titulo_columna_ventanillas': {'help_text': 'Título de la columna de ventanillas en la presentación.'},
        'limite_turnos_visibles_presentacion': {'help_text': 'Límite de turnos visibles en la presentación.'}
    }

class ColaEsperaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColaEspera
        fields = '__all__'