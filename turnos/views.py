from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import FranjaHoraria, Horario, Turnero, Menu
from .serializers import FranjaHorariaSerializer, HorarioSerializer, TurneroSerializer, TurneroMenuAssociationSerializer, MenuSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status



class FranjaHorariaViewSet(ModelViewSet):
    """
    CRUD para las franjas horarias.
    """
    queryset = FranjaHoraria.objects.all()
    serializer_class = FranjaHorariaSerializer
    permission_classes = [IsAuthenticated]


class HorarioViewSet(ModelViewSet):
    """
    API para gestionar asociaciones de franjas horarias con días de la semana.
    """
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    permission_classes = [IsAuthenticated]


class GenerarHorariosAPIView(APIView):
    """
    API para generar horarios de atención a partir de las configuraciones existentes.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Determinar el día actual en inglés y mapearlo al español
        dia_actual_en = datetime.now().strftime('%A').lower()
        dia_mapeo = {
            'monday': 'lunes',
            'tuesday': 'martes',
            'wednesday': 'miercoles',
            'thursday': 'jueves',
            'friday': 'viernes',
            'saturday': 'sabado',
            'sunday': 'domingo',
        }
        dia_actual_es = dia_mapeo[dia_actual_en]

        # Filtrar los horarios activos según el día actual
        horarios = Horario.objects.filter(**{dia_actual_es: True}).select_related('franja_horaria')

        # Construir la respuesta con horarios activos
        resultado = []
        for horario in horarios:
            franja = horario.franja_horaria
            resultado.append({
                "dia": dia_actual_es.capitalize(),
                "hora_inicio": str(franja.hora_inicio),
                "hora_fin": str(franja.hora_fin),
                "estado": franja.estado,
            })

        return Response({"horarios_activos": resultado})


class TurneroViewSet(viewsets.ModelViewSet):
    """
    API para gestionar los turneros.
    """
    queryset = Turnero.objects.all()
    serializer_class = TurneroSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='associate-menus')
    def associate_menus(self, request, pk=None):
        turnero = self.get_object()
        serializer = TurneroMenuAssociationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        menu_ids = serializer.validated_data.get('menu_ids', [])
        menus = Menu.objects.filter(id__in=menu_ids)
        turnero.menus.set(menus)

        return Response({
            "message": "Menús asociados correctamente.",
            "turnero": self.get_serializer(turnero).data
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='get-menus')
    def get_menus(self, request, pk=None):
        turnero = self.get_object()
        menus = turnero.menus.all()
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)