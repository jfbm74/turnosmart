from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from turnos.models import FranjaHoraria
from django.contrib.auth import get_user_model

User = get_user_model()

class FranjaHorariaAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        self.client.force_authenticate(user=self.user)

        # Crear una franja horaria inicial
        self.franja = FranjaHoraria.objects.create(
            hora_inicio="08:00:00",
            hora_fin="12:00:00",
            estado=True,
        )

        self.list_url = reverse("franja-horaria-list")
        self.detail_url = reverse("franja-horaria-detail", args=[self.franja.id])

    def test_list_franjas_authenticated(self):
        """Test para listar franjas horarias con autenticación."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_franjas_unauthenticated(self):
        """Test para listar franjas horarias sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_franja_authenticated(self):
        """Test para crear una franja horaria con autenticación."""
        data = {
            "hora_inicio": "13:00:00",
            "hora_fin": "17:00:00",
            "estado": True,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FranjaHoraria.objects.count(), 2)

    def test_create_franja_unauthenticated(self):
        """Test para crear una franja horaria sin autenticación."""
        self.client.force_authenticate(user=None)
        data = {
            "hora_inicio": "13:00:00",
            "hora_fin": "17:00:00",
            "estado": True,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_franja_authenticated(self):
        """Test para obtener una franja horaria específica con autenticación."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["hora_inicio"], self.franja.hora_inicio)

    def test_retrieve_franja_unauthenticated(self):
        """Test para obtener una franja horaria específica sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_franja_authenticated(self):
        """Test para actualizar una franja horaria con autenticación."""
        data = {
            "hora_inicio": "09:00:00",
            "hora_fin": "13:00:00",
            "estado": False,
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.franja.refresh_from_db()
        self.assertEqual(str(self.franja.hora_inicio), "09:00:00") 
        self.assertEqual(str(self.franja.hora_fin), "13:00:00") 


    def test_delete_franja_authenticated(self):
        """Test para eliminar una franja horaria con autenticación."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FranjaHoraria.objects.count(), 0)

    def test_delete_franja_unauthenticated(self):
        """Test para eliminar una franja horaria sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        FranjaHoraria.objects.all().delete()
        User.objects.all().delete()
