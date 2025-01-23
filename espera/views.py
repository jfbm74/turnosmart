from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Espera
from .serializers import EsperaSerializer

class EsperaViewSet(viewsets.ModelViewSet):
    """
    API para gestionar la configuración de mensajes de salas de espera.
    """
    queryset = Espera.objects.all()
    serializer_class = EsperaSerializer
    permission_classes = [IsAuthenticated]
