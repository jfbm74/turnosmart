import os
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from backend import settings
from configuracion.models import Institucion, Imagen 
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

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
        response = self.client.post(
            reverse("api_token_auth"),  # Endpoint para obtener el token
            {"username": "admin", "password": "123456"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        token = response.data.get("token")
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


class ImagenAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Crear usuarios
        self.admin_user = User.objects.create_superuser(
            username="admin", password="123456", email="admin@example.com"
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )

        # Crear una imagen inicial
        self.imagen = Imagen.objects.create(
            logo_pequeño="images/small_logo.png",
            logo_grande="images/large_logo.png",
            logo_ticket="images/ticket_logo.png",
            footer="images/footer.png",
            wallpaper_turnero="images/wallpaper.png",
        )

        self.list_url = reverse("imagen-list")
        self.detail_url = reverse("imagen-detail", args=[self.imagen.id])

    def authenticate(self):
        response = self.client.post(
            reverse("api_token_auth"), 
            {"username": "admin", "password": "123456"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        token = response.data.get("token")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    def test_list_imagenes_authenticated(self):
        """Test para listar imágenes con autenticación."""
        self.authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_imagen_authenticated(self):
        """Test para crear una imagen con autenticación."""
        self.authenticate()
        def create_test_image(filename):
            image = Image.new('RGB', (100, 100), color='red')
            byte_arr = io.BytesIO()
            image.save(byte_arr, format='PNG')
            return SimpleUploadedFile(filename, byte_arr.getvalue(), content_type='image/png')

        data = {
            "logo_pequeño": create_test_image("small_logo.png"),
            "logo_grande": create_test_image("large_logo.png"),
        }

        response = self.client.post(self.list_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Imagen.objects.count(), 2)
