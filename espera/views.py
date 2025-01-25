from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Espera
from .serializers import EsperaSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status


class EsperaViewSet(viewsets.ModelViewSet):
    """
    API para gestionar la configuración de mensajes de salas de espera.
    """
    queryset = Espera.objects.all()
    serializer_class = EsperaSerializer
    permission_classes = [IsAuthenticated]


class EsperaViewSet(viewsets.ModelViewSet):
    """
    API para gestionar la configuración de mensajes de salas de espera.
    """
    queryset = Espera.objects.all()
    serializer_class = EsperaSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: EsperaSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """Listar todas las configuraciones de espera"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=EsperaSerializer,
        responses={status.HTTP_201_CREATED: EsperaSerializer()}
    )
    def create(self, request, *args, **kwargs):
        """Crear una nueva configuración de espera"""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: EsperaSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        """Ver una configuración de espera por ID"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body = EsperaSerializer,
        responses={status.HTTP_200_OK: EsperaSerializer()}
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
