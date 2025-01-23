from rest_framework.routers import DefaultRouter
from .views import EsperaViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'esperas', EsperaViewSet, basename='espera')

urlpatterns = router.urls