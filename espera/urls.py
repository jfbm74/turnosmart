from rest_framework.routers import DefaultRouter
from .views import ColaEsperaViewSet, EsperaViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'esperas', EsperaViewSet, basename='espera')
router.register(r'colas-espera', ColaEsperaViewSet, basename='cola-espera')

urlpatterns = [
    path('', include(router.urls)),
]