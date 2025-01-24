from rest_framework.routers import DefaultRouter
from .views import FranjaHorariaViewSet, HorarioViewSet

router = DefaultRouter()
router.register(r'franjas-horarias', FranjaHorariaViewSet, basename='franja-horaria')
router.register(r'horarios', HorarioViewSet, basename='horario')

urlpatterns = router.urls
