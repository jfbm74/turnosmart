from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from apps.turnos.models import FranjaHoraria, Horario, Prioridad, Turnero, Menu, Sala
from apps.core.models import Tramite
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
    


class HorariosListView(ListView):
    """
    Vista para listar los horarios y franjas horarias en el frontend.
    """
    model = Horario
    template_name = "turnos/app-horarios-list-view.html"
    context_object_name = "schedules"

    def get_queryset(self):
        # Usar select_related para obtener los datos de la franja horaria en una sola consulta
        return Horario.objects.select_related('franja_horaria').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # También optimizamos la consulta de franjas horarias
        context["franjas_horarias"] = FranjaHoraria.objects.all()
        return context
    


class TurneroViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar turneros.
    """
    queryset = Turnero.objects.all()
    serializer_class = TurneroSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete'] 

    @swagger_auto_schema(
        operation_description="Listar todos los turneros",
        responses={200: TurneroSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crear un nuevo turnero",
        request_body=TurneroSerializer,
        responses={
            201: TurneroSerializer(),
            400: "Bad Request"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={200: TurneroSerializer()},
        operation_description="Obtener un turnero específico"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=TurneroSerializer,
        responses={200: TurneroSerializer()},
        operation_description="Actualizar un turnero"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={204: "No Content"},
        operation_description="Eliminar un turnero"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='associate-menus')
    def associate_menus(self, request, pk=None):
        turnero = self.get_object()
        menu_ids = request.data.get('menu_ids', [])
        menus = Menu.objects.filter(id__in=menu_ids)
        turnero.menus.set(menus)
        return Response(self.get_serializer(turnero).data)

    @action(detail=True, methods=['get'], url_path='get-menus')
    def get_menus(self, request, pk=None):
        turnero = self.get_object()
        menus = turnero.menus.all()
        menu_serializer = MenuSerializer(menus, many=True)
        return Response(menu_serializer.data)



class TurneroListView(LoginRequiredMixin, ListView):
    model = Turnero
    template_name = "turnos/app-turnero-list-view.html"
    context_object_name = "turneros"

    def get_queryset(self):
        return Turnero.objects.all().prefetch_related('menus')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menus"] = Menu.objects.all()
        return context
    



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


class MenuViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Menus to be viewed and edited.
    """

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="List all Menus")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new Menu",
        request_body=MenuSerializer,
        responses={
            status.HTTP_201_CREATED: MenuSerializer(),
            status.HTTP_400_BAD_REQUEST: "Bad Request",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a Menu by ID",
        responses={
            status.HTTP_200_OK: MenuSerializer(),
            status.HTTP_404_NOT_FOUND: "Not Found",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a Menu by ID",
        request_body=MenuSerializer,
        responses={
            status.HTTP_200_OK: MenuSerializer(),
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_404_NOT_FOUND: "Not Found",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a Menu by ID",
        request_body=MenuSerializer(partial=True),
        responses={
            status.HTTP_200_OK: MenuSerializer(),
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_404_NOT_FOUND: "Not Found",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a Menu by ID",
        responses={
            status.HTTP_204_NO_CONTENT: "No Content",
            status.HTTP_404_NOT_FOUND: "Not Found",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class MenuListView(LoginRequiredMixin, ListView):
    model = Menu
    template_name = "turnos/app-menu-list-view.html"  # Updated template path
    context_object_name = "menus"
    login_url = '/account/login/'  # Optional, specify the login URL if needed
    redirect_field_name = 'redirect_to'  # Optional, specify your redirect field name

    def get_queryset(self):
        return Menu.objects.all().select_related('prioridad')  # Optimizes the database query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prioridades"] = Prioridad.objects.all()  # Passes all priorities for the modal select
        context["tramites"] = Tramite.objects.all()  # Passes all Tramites to the template
        return context