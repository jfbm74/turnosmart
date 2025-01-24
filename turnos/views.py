from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import FranjaHoraria
from .serializers import FranjaHorariaSerializer

class FranjaHorariaViewSet(ModelViewSet):
    """
    CRUD para las franjas horarias.
    """
    queryset = FranjaHoraria.objects.all()
    serializer_class = FranjaHorariaSerializer
    permission_classes = [IsAuthenticated]
