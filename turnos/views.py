from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import FranjaHoraria, Horario
from .serializers import FranjaHorariaSerializer, HorarioSerializer

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