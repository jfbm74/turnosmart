#  apps/configuracion/views.py

import os
from django.views import View
from rest_framework import viewsets
from django.views.generic import ListView
from django.shortcuts import render
import requests
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
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required





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
        """
        Create a new Institucion.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@login_required(login_url='/login/')
def instituciones_list_view(request):
    """
    Vista para consumir la API de instituciones y renderizar un template.
    """
    # URL de la API de instituciones
    permission_classes = [IsAuthenticated] 
    api_url = f"{settings.API_BASE_URL}/instituciones/"
    headers = {
        "Authorization": f"Token {settings.API_AUTH_TOKEN}"  # Asegúrate de configurar esto en settings.py
    }

    # Realizar la solicitud a la API
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            instituciones = response.json()  # Convertir la respuesta a JSON
        else:
            instituciones = []
    except requests.RequestException as e:
        instituciones = []  # Manejo de errores en caso de fallo de conexión
        print(f"Error al conectar con la API: {e}")

    # Renderizar el template con los datos
    return render(
        request,
        "configuracion/app-institucion-list-view.html",
        {"instituciones": instituciones}
    )

class InstitucionListView(LoginRequiredMixin, ListView):
    model = Institucion
    template_name = "configuracion/app-institucion-list-view.html"
    context_object_name = "instituciones"


class ImagenViewSet(viewsets.ModelViewSet):
    """
    API para gestionar imágenes.
    """
    queryset = Imagen.objects.all()
    serializer_class = ImagenSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

class ImagenListView(LoginRequiredMixin, ListView):
    model = Imagen
    template_name = "configuracion/app-imagen-list-view.html"  # Ruta de la plantilla
    context_object_name = "imagenes"



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


class VideoListView(LoginRequiredMixin, ListView):
    model = Video
    template_name = "configuracion/app-video-list-view.html" 
    context_object_name = "videos"



class AudioViewSet(viewsets.ModelViewSet):
    """
    API para gestionar audios.
    """
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer


class AudioListView(LoginRequiredMixin, ListView):
    model = Audio
    template_name = "configuracion/app-audio-list-view.html"  # Ruta del template
    context_object_name = "audios"


class TicketViewSet(viewsets.ModelViewSet):
    """
    API para gestionar configuración de tickets.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketListView(ListView):
    model = Ticket
    template_name = "configuracion/app-ticket-list-view.html"  # Corregido
    context_object_name = "tickets"




class TicketPreviewView(TemplateView):
    template_name = 'configuracion/app-ticket-preview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs.get('pk')  # Obtenemos el ID del ticket desde la URL
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        context['ticket'] = ticket
        return context


class SistemaViewSet(viewsets.ModelViewSet):
    """
    API para gestionar configuración del sistema.
    """
    queryset = Sistema.objects.all()
    serializer_class = SistemaSerializer


class SistemaListView(LoginRequiredMixin, ListView):
    model = Sistema
    template_name = "configuracion/app-system-list-view.html"
    context_object_name = "sistema"  # Cambiado de sistema_config
    
    def get_queryset(self):
        """
        Returns the single existing object or creates one if it doesn't exist
        """
        sistema, created = Sistema.objects.get_or_create(pk=1)
        return sistema  # Retornamos el objeto directamente, no una lista


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




