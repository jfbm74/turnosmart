from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Espera, ColaEspera
from .serializers import EsperaSerializer, ColaEsperaSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class EsperaViewSet(viewsets.ModelViewSet):
    """
    API para gestionar la configuración de mensajes de salas de espera.
    """

    queryset = Espera.objects.all()
    serializer_class = EsperaSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={status.HTTP_200_OK: EsperaSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        """Listar todas las configuraciones de espera"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=EsperaSerializer,
        responses={status.HTTP_201_CREATED: EsperaSerializer()},
    )
    def create(self, request, *args, **kwargs):
        """Crear una nueva configuración de espera"""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: EsperaSerializer()})
    def retrieve(self, request, *args, **kwargs):
        """Ver una configuración de espera por ID"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=EsperaSerializer,
        responses={status.HTTP_200_OK: EsperaSerializer()},
    )
    def update(self, request, *args, **kwargs):
        """Editar una configuración de espera por ID"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: "Configuración de espera eliminada"}
    )
    def destroy(self, request, *args, **kwargs):
        """Eliminar una configuración de espera por ID"""
        return super().destroy(request, *args, **kwargs)


class ColaEsperaViewSet(viewsets.ModelViewSet):
    queryset = ColaEspera.objects.all()
    serializer_class = ColaEsperaSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"], url_path="get-cola")
    def get_cola(self, request, pk=None):
        cola = self.get_object()
        return Response(
            {
                "sala": cola.sala.nombre,
                "turnos": [
                    {
                        "numero": "A001",
                        "tramite": "Consulta General",
                        "estado": "En espera",
                    },
                    {"numero": "A002", "tramite": "Laboratorio", "estado": "En espera"},
                ],
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="configurar-cola")
    def configurar_cola(self, request, pk=None):
        cola = self.get_object()
        serializer = self.get_serializer(instance=cola, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
