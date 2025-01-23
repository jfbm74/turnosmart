from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from espera.models import Espera
from django.contrib.auth import get_user_model

User = get_user_model()


class EsperaAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        self.client.force_authenticate(user=self.user)

        # Crear una configuración inicial de espera
        self.espera = Espera.objects.create(
            llamado_sala_espera_individual="@ turno. {turno_dividido} pase a. {ventanilla}",
            llamado_sala_espera_multiple_parte1="Turnos:",
            llamado_sala_espera_multiple_parte2="{turno_dividido}",
            llamado_sala_espera_multiple_parte3="pasen a. {ventanilla}",
            titulo_columna_turnos="TURNO",
            titulo_columna_espera="ESPERA",
            titulo_columna_ventanillas="SERVICIO",
            limite_turnos_visibles_presentacion=7,
        )

        self.list_url = reverse("espera-list")
        self.detail_url = reverse("espera-detail", args=[self.espera.id])

    def test_list_espera_authenticated(self):
        """Test para listar configuraciones de espera con autenticación."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_espera_unauthenticated(self):
        """Test para listar configuraciones de espera sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_espera_authenticated(self):
        """Test para crear una configuración de espera con autenticación."""
        data = {
            "llamado_sala_espera_individual": "@ turno {turno_dividido} pase a {ventanilla}",
            "llamado_sala_espera_multiple_parte1": "Turnos:",
            "llamado_sala_espera_multiple_parte2": "{turno_dividido}",
            "llamado_sala_espera_multiple_parte3": "pasen a {ventanilla}",
            "titulo_columna_turnos": "TURNO",
            "titulo_columna_espera": "ESPERA",
            "titulo_columna_ventanillas": "SERVICIO",
            "limite_turnos_visibles_presentacion": 10,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Espera.objects.count(), 2)

    def test_create_espera_unauthenticated(self):
        """Test para crear una configuración de espera sin autenticación."""
        self.client.force_authenticate(user=None)
        data = {
            "llamado_sala_espera_individual": "@ turno {turno_dividido} pase a {ventanilla}",
            "llamado_sala_espera_multiple_parte1": "Turnos:",
            "llamado_sala_espera_multiple_parte2": "{turno_dividido}",
            "llamado_sala_espera_multiple_parte3": "pasen a {ventanilla}",
            "titulo_columna_turnos": "TURNO",
            "titulo_columna_espera": "ESPERA",
            "titulo_columna_ventanillas": "SERVICIO",
            "limite_turnos_visibles_presentacion": 10,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_espera_authenticated(self):
        """Test para obtener una configuración específica de espera con autenticación."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["titulo_columna_turnos"], self.espera.titulo_columna_turnos)

    def test_retrieve_espera_unauthenticated(self):
        """Test para obtener una configuración específica de espera sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_espera_authenticated(self):
        """Test para actualizar una configuración de espera con autenticación."""
        data = {
            "llamado_sala_espera_individual": "@ turno actualizado {turno_dividido} pase a {ventanilla}",
            "titulo_columna_turnos": "TURNO ACTUALIZADO",
        }
        response = self.client.patch(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.espera.refresh_from_db()
        self.assertEqual(self.espera.titulo_columna_turnos, "TURNO ACTUALIZADO")

    def test_delete_espera_authenticated(self):
        """Test para eliminar una configuración de espera con autenticación."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Espera.objects.count(), 0)

    def test_delete_espera_unauthenticated(self):
        """Test para eliminar una configuración de espera sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        Espera.objects.all().delete()
        User.objects.all().delete()
