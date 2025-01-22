from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from configuracion.models import Institucion

User = get_user_model()

class InstitucionAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Crear usuarios
        self.admin_user = User.objects.create_superuser(
            username="admin", password="123456", email="admin@example.com"
        )
        self.test_user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
        )

        # Crear institución inicial
        self.institucion = Institucion.objects.create(
            nombre="Institución de Prueba",
            siglas="IDP",
            direccion="Dirección de Prueba",
            ubicacion="Ubicación de Prueba",
            telefono="123456789",
            email="institucion@example.com",
            sitio_web="http://example.com",
            mensaje="Mensaje de prueba",
        )

        self.list_url = reverse("institucion-list")
        self.detail_url = reverse("institucion-detail", args=[self.institucion.id])

    def authenticate(self):
        login_response = self.client.post(
            reverse("login"), {"username": "admin", "password": "123456"}, format="json"
        )
        token = login_response.data.get("token")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    def test_list_instituciones_authenticated(self):
        """Test para listar instituciones con autenticación."""
        self.authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_instituciones_unauthenticated(self):
        """Test para listar instituciones sin autenticación."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_institucion_authenticated(self):
        """Test para crear una institución con autenticación."""
        self.authenticate()
        data = {
            "nombre": "Nueva Institución",
            "siglas": "NI",
            "direccion": "Nueva Dirección",
            "ubicacion": "Nueva Ubicación",
            "telefono": "987654321",
            "email": "nueva@example.com",
            "sitio_web": "http://nueva.com",
            "mensaje": "Nuevo mensaje",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Institucion.objects.count(), 2)

    def test_create_institucion_unauthenticated(self):
        """Test para crear una institución sin autenticación."""
        data = {
            "nombre": "Nueva Institución",
            "siglas": "NI",
            "direccion": "Nueva Dirección",
            "ubicacion": "Nueva Ubicación",
            "telefono": "987654321",
            "email": "nueva@example.com",
            "sitio_web": "http://nueva.com",
            "mensaje": "Nuevo mensaje",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_institucion_authenticated(self):
        """Test para obtener una institución específica con autenticación."""
        self.authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nombre"], self.institucion.nombre)

    def test_retrieve_institucion_unauthenticated(self):
        """Test para obtener una institución específica sin autenticación."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_institucion_authenticated(self):
        """Test para actualizar una institución con autenticación."""
        self.authenticate()
        data = {
            "nombre": "Institución Actualizada",
            "siglas": "IA",
            "direccion": "Dirección Actualizada",
            "ubicacion": "Ubicación Actualizada",
            "telefono": "123123123",
            "email": "actualizada@example.com",
            "sitio_web": "http://actualizada.com",
            "mensaje": "Mensaje actualizado",
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.institucion.refresh_from_db()
        self.assertEqual(self.institucion.nombre, "Institución Actualizada")

    def test_delete_institucion_authenticated(self):
        """Test para eliminar una institución con autenticación."""
        self.authenticate()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Institucion.objects.count(), 0)

    def test_delete_institucion_unauthenticated(self):
        """Test para eliminar una institución sin autenticación."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
