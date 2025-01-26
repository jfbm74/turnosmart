# configuracion/views.py

import os
from rest_framework import viewsets

from velzon import settings
from .models import Institucion, Imagen, Video, Audio, Ticket, Sistema, Voz
from .serializers import (
    InstitucionSerializer,
    ImagenSerializer,
    VideoSerializer,
    AudioSerializer,
    TicketSerializer,
    SistemaSerializer,
    VozSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status



class InstitucionViewSet(viewsets.ModelViewSet):
    """
    API para gestionar instituciones.
    """
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer
    permission_classes = [IsAuthenticated] 

    @swagger_auto_schema(operation_description="Listar todas las instituciones.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Crear una nueva institución.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ImagenViewSet(viewsets.ModelViewSet):
    """
    API para gestionar imágenes.
    """
    queryset = Imagen.objects.all()
    serializer_class = ImagenSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        images_dir = os.path.join(settings.MEDIA_ROOT, 'images')
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)


class VideoViewSet(viewsets.ModelViewSet):
    """
    API para gestionar videos.
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(
          request_body=VideoSerializer,
            responses={status.HTTP_201_CREATED: VideoSerializer()}
    )
    def create(self, request, *args, **kwargs):
            """Crea un video. """
            return super().create(request, *args, **kwargs)


    @swagger_auto_schema(
            responses={status.HTTP_200_OK: VideoSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
              """Lista todos los videos del sistema"""
              return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
          responses={status.HTTP_200_OK: VideoSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
           """Obtener información del video por su ID"""
           return super().retrieve(request, *args, **kwargs)


    @swagger_auto_schema(
        request_body = VideoSerializer,
                responses={status.HTTP_200_OK: VideoSerializer()}
    )
    def update(self, request, *args, **kwargs):
            """Actualiza la información del video por ID"""
            return super().update(request, *args, **kwargs)


    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: "Video eliminado"}
    )
    def destroy(self, request, *args, **kwargs):
        """Elimina un video por ID"""
        return super().destroy(request, *args, **kwargs)
        
    @action(detail=False, methods=['post'])
    @swagger_auto_schema(operation_description="Validar URL de video.")
    def validar_url(self, request):
            """Verifica la validez de la URL del video"""
            url = request.data.get("url_video", None)
            if not url:
                 return Response({"error": "Debe proporcionar una URL."}, status=400)
            return Response({"mensaje": "URL válida."}, status=200)


class AudioViewSet(viewsets.ModelViewSet):
    """
    API para gestionar audios.
    """
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer


class TicketViewSet(viewsets.ModelViewSet):
    """
    API para gestionar configuración de tickets.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class SistemaViewSet(viewsets.ModelViewSet):
    """
    API para gestionar configuración del sistema.
    """
    queryset = Sistema.objects.all()
    serializer_class = SistemaSerializer


class VozViewSet(viewsets.ModelViewSet):
    """
    API para gestionar configuración de voz.
    """
    queryset = Voz.objects.all()
    serializer_class = VozSerializer



class ImagenViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ImagenSerializer
    queryset = Imagen.objects.all()