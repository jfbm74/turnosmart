from rest_framework.routers import DefaultRouter
from .views import FranjaHorariaViewSet

router = DefaultRouter()
router.register(r'franjas-horarias', FranjaHorariaViewSet, basename='franja-horaria')

urlpatterns = router.urls
