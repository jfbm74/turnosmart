import os
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from backend import settings
from configuracion.models import Institucion, Imagen, Video, Audio, Ticket, Sistema, Voz
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
    
    def tearDown(self):
        Institucion.objects.all().delete()
        User.objects.all().delete()


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
    
    def tearDown(self):
        Imagen.objects.all().delete()
        User.objects.all().delete()


class VideoAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        self.client.force_authenticate(user=self.user)

        # Crear un video inicial
        self.video = Video.objects.create(
            origen="URL",
            url_video="http://example.com/video.mp4",
            estado=True,
        )

        self.list_url = reverse("video-list")
        self.detail_url = reverse("video-detail", args=[self.video.id])

    def test_list_videos_authenticated(self):
        """Test para listar videos con autenticación."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_videos_unauthenticated(self):
        """Test para listar videos sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_video_authenticated(self):
        """Test para crear un video con autenticación."""
        data = {
            "origen": "URL",
            "url_video": "http://example.com/new_video.mp4",
            "estado": True,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Video.objects.count(), 2)

    def test_create_video_unauthenticated(self):
        """Test para crear un video sin autenticación."""
        self.client.force_authenticate(user=None)
        data = {
            "origen": "URL",
            "url_video": "http://example.com/new_video.mp4",
            "estado": True,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_video_authenticated(self):
        """Test para obtener un video específico con autenticación."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["url_video"], self.video.url_video)

    def test_retrieve_video_unauthenticated(self):
        """Test para obtener un video específico sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_video_authenticated(self):
        """Test para actualizar un video con autenticación."""
        data = {
            "origen": "URL",
            "url_video": "http://example.com/updated_video.mp4",
            "estado": False,
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.video.refresh_from_db()
        self.assertEqual(self.video.url_video, "http://example.com/updated_video.mp4")

    def test_delete_video_authenticated(self):
        """Test para eliminar un video con autenticación."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Video.objects.count(), 0)

    def test_delete_video_unauthenticated(self):
        """Test para eliminar un video sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def tearDown(self):
        Video.objects.all().delete()
        User.objects.all().delete()


class AudioAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        self.client.force_authenticate(user=self.user)

        # Crear un audio inicial
        self.audio = Audio.objects.create(
            timbre=SimpleUploadedFile("test_audio.mp3", b"file_content")
        )

        self.list_url = reverse("audio-list")
        self.detail_url = reverse("audio-detail", args=[self.audio.id])

    def test_list_audios_authenticated(self):
        """Test para listar audios con autenticación."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_audios_unauthenticated(self):
        """Test para listar audios sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_audio_authenticated(self):
        """Test para crear un audio con autenticación."""
        data = {
            "timbre": SimpleUploadedFile("new_audio.mp3", b"new_file_content"),
        }
        response = self.client.post(self.list_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Audio.objects.count(), 2)

    def test_create_audio_unauthenticated(self):
        """Test para crear un audio sin autenticación."""
        self.client.force_authenticate(user=None)
        data = {
            "timbre": SimpleUploadedFile("new_audio.mp3", b"new_file_content"),
        }
        response = self.client.post(self.list_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_audio_authenticated(self):
        """Test para obtener un audio específico con autenticación."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_audio_unauthenticated(self):
        """Test para obtener un audio específico sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_audio_authenticated(self):
        """Test para actualizar un audio con autenticación."""
        data = {
            "timbre": SimpleUploadedFile("updated_audio.mp3", b"updated_file_content"),
        }
        response = self.client.put(self.detail_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_audio_authenticated(self):
        """Test para eliminar un audio con autenticación."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Audio.objects.count(), 0)

    def test_delete_audio_unauthenticated(self):
        """Test para eliminar un audio sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def tearDown(self):
        Audio.objects.all().delete()
        User.objects.all().delete()


class TicketAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        self.client.force_authenticate(user=self.user)

        # Crear una configuración inicial de ticket
        self.ticket = Ticket.objects.create(
            ancho_ticket=80,
            ancho_logo=35,
            logo_visible=True,
            fuente_turno=14,
            fuente_tramite=5,
            tramite_visible=True,
        )

        self.list_url = reverse("ticket-list")
        self.detail_url = reverse("ticket-detail", args=[self.ticket.id])

    def test_list_tickets_authenticated(self):
        """Test para listar configuraciones de tickets con autenticación."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_tickets_unauthenticated(self):
        """Test para listar configuraciones de tickets sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_ticket_authenticated(self):
        """Test para crear una configuración de ticket con autenticación."""
        data = {
            "ancho_ticket": 90,
            "ancho_logo": 40,
            "logo_visible": True,
            "fuente_turno": 16,
            "fuente_tramite": 6,
            "tramite_visible": True,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 2)

    def test_create_ticket_unauthenticated(self):
        """Test para crear una configuración de ticket sin autenticación."""
        self.client.force_authenticate(user=None)
        data = {
            "ancho_ticket": 90,
            "ancho_logo": 40,
            "logo_visible": True,
            "fuente_turno": 16,
            "fuente_tramite": 6,
            "tramite_visible": True,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_ticket_authenticated(self):
        """Test para obtener una configuración específica de ticket con autenticación."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["ancho_ticket"], self.ticket.ancho_ticket)

    def test_retrieve_ticket_unauthenticated(self):
        """Test para obtener una configuración específica de ticket sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_ticket_authenticated(self):
        """Test para actualizar una configuración de ticket con autenticación."""
        data = {
            "ancho_ticket": 100,
            "ancho_logo": 45,
            "logo_visible": False,
            "fuente_turno": 18,
            "fuente_tramite": 7,
            "tramite_visible": False,
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.ancho_ticket, 100)

    def test_delete_ticket_authenticated(self):
        """Test para eliminar una configuración de ticket con autenticación."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ticket.objects.count(), 0)

    def test_delete_ticket_unauthenticated(self):
        """Test para eliminar una configuración de ticket sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def tearDown(self):
        Ticket.objects.all().delete()
        User.objects.all().delete()


class SistemaAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        self.client.force_authenticate(user=self.user)

        # Crear una configuración inicial del sistema
        self.sistema = Sistema.objects.create(
            tiempo_espera=10,
            umbral_espera=5,
            mostrar_turnos_anulados=True,
            mostrar_turnos_atendidos=False,
            num_max_turnos_cedula=3,
            version_sistema="4.0.1",
        )

        self.list_url = reverse("sistema-list")
        self.detail_url = reverse("sistema-detail", args=[self.sistema.id])

    def test_list_sistema_authenticated(self):
        """Test para listar configuraciones del sistema con autenticación."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_sistema_unauthenticated(self):
        """Test para listar configuraciones del sistema sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_sistema_authenticated(self):
        """Test para crear una configuración del sistema con autenticación."""
        data = {
            "tiempo_espera": 15,
            "umbral_espera": 7,
            "mostrar_turnos_anulados": False,
            "mostrar_turnos_atendidos": True,
            "num_max_turnos_cedula": 5,
            "version_sistema": "4.0.2",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sistema.objects.count(), 2)

    def test_create_sistema_unauthenticated(self):
        """Test para crear una configuración del sistema sin autenticación."""
        self.client.force_authenticate(user=None)
        data = {
            "tiempo_espera": 15,
            "umbral_espera": 7,
            "mostrar_turnos_anulados": False,
            "mostrar_turnos_atendidos": True,
            "num_max_turnos_cedula": 5,
            "version_sistema": "4.0.2",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_sistema_authenticated(self):
        """Test para obtener una configuración del sistema específica con autenticación."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["tiempo_espera"], self.sistema.tiempo_espera)

    def test_retrieve_sistema_unauthenticated(self):
        """Test para obtener una configuración del sistema específica sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_sistema_authenticated(self):
        """Test para actualizar una configuración del sistema con autenticación."""
        data = {
            "tiempo_espera": 20,
            "umbral_espera": 10,
            "mostrar_turnos_anulados": True,
            "mostrar_turnos_atendidos": True,
            "num_max_turnos_cedula": 10,
            "version_sistema": "4.1.0",
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.sistema.refresh_from_db()
        self.assertEqual(self.sistema.tiempo_espera, 20)

    def test_delete_sistema_authenticated(self):
        """Test para eliminar una configuración del sistema con autenticación."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Sistema.objects.count(), 0)

    def test_delete_sistema_unauthenticated(self):
        """Test para eliminar una configuración del sistema sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        Sistema.objects.all().delete()
        User.objects.all().delete()

class VozAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        self.client.force_authenticate(user=self.user)

        # Crear una configuración inicial de voz
        self.voz = Voz.objects.create(
            llamado_turno_con_voz=True,
            origen_voz="TTS NAVEGADOR WEB",
            idioma="ESPAÑOL (ESPAÑA)",
            tono=1.2,
            velocidad=1.0,
            volumen=0.8,
        )

        self.list_url = reverse("voz-list")
        self.detail_url = reverse("voz-detail", args=[self.voz.id])

    def test_list_vozes_authenticated(self):
        """Test para listar configuraciones de voz con autenticación."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_vozes_unauthenticated(self):
        """Test para listar configuraciones de voz sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_voz_authenticated(self):
        """Test para crear una configuración de voz con autenticación."""
        data = {
            "llamado_turno_con_voz": False,
            "origen_voz": "URL EXTERNA",
            "idioma": "INGLÉS (EEUU)",
            "tono": 1.0,
            "velocidad": 1.5,
            "volumen": 1.0,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Voz.objects.count(), 2)

    def test_create_voz_unauthenticated(self):
        """Test para crear una configuración de voz sin autenticación."""
        self.client.force_authenticate(user=None)
        data = {
            "llamado_turno_con_voz": False,
            "origen_voz": "URL EXTERNA",
            "idioma": "INGLÉS (EEUU)",
            "tono": 1.0,
            "velocidad": 1.5,
            "volumen": 1.0,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_voz_authenticated(self):
        """Test para obtener una configuración de voz específica con autenticación."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["idioma"], self.voz.idioma)

    def test_retrieve_voz_unauthenticated(self):
        """Test para obtener una configuración de voz específica sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_voz_authenticated(self):
        """Test para actualizar una configuración de voz con autenticación."""
        data = {
            "tono": 1.5,
            "velocidad": 0.9,
            "volumen": 0.7,
        }
        response = self.client.patch(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.voz.refresh_from_db()
        self.assertEqual(self.voz.tono, 1.5)

    def test_delete_voz_authenticated(self):
        """Test para eliminar una configuración de voz con autenticación."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Voz.objects.count(), 0)

    def test_delete_voz_unauthenticated(self):
        """Test para eliminar una configuración de voz sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        Voz.objects.all().delete()
        User.objects.all().delete()