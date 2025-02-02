from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from apps.turnos.models import FranjaHoraria, Horario, Prioridad, Turnero, Menu, Sala
from .serializers import (
    FranjaHorariaSerializer,
    HorarioSerializer,
    PrioridadSerializer,
    TurneroSerializer,
    TurneroMenuAssociationSerializer,
    MenuSerializer,
    SalaSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView




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
        dia_actual_en = datetime.now().strftime("%A").lower()
        dia_mapeo = {
            "monday": "lunes",
            "tuesday": "martes",
            "wednesday": "miercoles",
            "thursday": "jueves",
            "friday": "viernes",
            "saturday": "sabado",
            "sunday": "domingo",
        }
        dia_actual_es = dia_mapeo[dia_actual_en]

        # Filtrar los horarios activos según el día actual
        horarios = Horario.objects.filter(**{dia_actual_es: True}).select_related(
            "franja_horaria"
        )

        # Construir la respuesta con horarios activos
        resultado = []
        for horario in horarios:
            franja = horario.franja_horaria
            resultado.append(
                {
                    "dia": dia_actual_es.capitalize(),
                    "hora_inicio": str(franja.hora_inicio),
                    "hora_fin": str(franja.hora_fin),
                    "estado": franja.estado,
                }
            )

        return Response({"horarios_activos": resultado})


class TurneroViewSet(viewsets.ModelViewSet):
    """
    API para gestionar los turneros.
    """

    queryset = Turnero.objects.all()
    serializer_class = TurneroSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"], url_path="associate-menus")
    def associate_menus(self, request, pk=None):
        turnero = self.get_object()
        serializer = TurneroMenuAssociationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        menu_ids = serializer.validated_data.get("menu_ids", [])
        menus = Menu.objects.filter(id__in=menu_ids)
        turnero.menus.set(menus)

        return Response(
            {
                "message": "Menús asociados correctamente.",
                "turnero": self.get_serializer(turnero).data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"], url_path="get-menus")
    def get_menus(self, request, pk=None):
        turnero = self.get_object()
        menus = turnero.menus.all()
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)


class SalaViewSet(ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [IsAuthenticated]


class PrioridadViewSet(viewsets.ModelViewSet):
    """
    API para gestionar las prioridades.
    """
    queryset = Prioridad.objects.all()
    serializer_class = PrioridadSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(operation_description="Listar las prioridades")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea una nueva prioridad",
        request_body=PrioridadSerializer,
        responses={
            status.HTTP_201_CREATED: PrioridadSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid data",
        },
    )
    def create(self, request, *args, **kwargs):
       return super().create(request, *args, **kwargs)


    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: PrioridadSerializer(),
            status.HTTP_404_NOT_FOUND: "Prioridad no encontrada",
        },
        operation_description="Obtener una prioridad especifica por id"
    )
    def retrieve(self, request, *args, **kwargs):
         return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
         request_body=PrioridadSerializer,
            responses={
                status.HTTP_200_OK: PrioridadSerializer(),
                status.HTTP_400_BAD_REQUEST: "Invalid data",
                status.HTTP_404_NOT_FOUND: "Prioridad no encontrada"
           },
        operation_description="Actualizar una prioridad existente"
    )
    def update(self, request, *args, **kwargs):
         return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
           responses={
               status.HTTP_204_NO_CONTENT: "Prioridad eliminada exitosamente",
                status.HTTP_404_NOT_FOUND: "Prioridad no encontrada"
            },
        operation_description="Eliminar una prioridad existente"
    )
    def destroy(self, request, *args, **kwargs):
         return super().destroy(request, *args, **kwargs)


class PrioridadListView(LoginRequiredMixin, ListView):
    model = Prioridad
    template_name = "turnos/app-prioridad-list-view.html"  # Ruta del template
    context_object_name = "prioridades"