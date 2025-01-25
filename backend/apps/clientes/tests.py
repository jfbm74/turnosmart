from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from backend.apps.clientes.models import Cliente
from django.contrib.auth import get_user_model

User = get_user_model()


class ClienteAPITests(APITestCase):
    def setUp(self):

        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
        )
        self.client.force_authenticate(user=self.user)

        self.cliente = Cliente.objects.create(
            nombre="Juan",
            apellido="Pérez",
            documento="12345678",
            email="juan.perez@example.com",
            direccion="Calle Falsa 123",
            telefono="123456789",
            estado=True,
        )

        self.list_create_url = reverse("clientes_list_create")
        self.detail_url = reverse("clientes_detail", kwargs={"pk": self.cliente.id})

    def test_list_clientes_authenticated(self):
        """Test para listar clientes con usuario autenticado"""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_clientes_unauthenticated(self):
        """Test para listar clientes sin autenticación"""
        self.client.force_authenticate(user=None)  # Eliminar autenticación
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_cliente_authenticated(self):
        """Test para crear un cliente con usuario autenticado"""
        data = {
            "nombre": "Ana",
            "apellido": "García",
            "documento": "87654321",
            "email": "ana.garcia@example.com",
            "direccion": "Avenida Siempreviva 742",
            "telefono": "987654321",
            "estado": True,
        }
        response = self.client.post(self.list_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Cliente creado exitosamente")

    def test_create_cliente_unauthenticated(self):
        """Test para crear un cliente sin autenticación"""
        self.client.force_authenticate(user=None)  # Eliminar autenticación
        data = {
            "nombre": "Ana",
            "apellido": "García",
            "documento": "87654321",
            "email": "ana.garcia@example.com",
            "direccion": "Avenida Siempreviva 742",
            "telefono": "987654321",
            "estado": True,
        }
        response = self.client.post(self.list_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_cliente_authenticated(self):
        """Test para obtener un cliente con usuario autenticado"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nombre"], self.cliente.nombre)

    def test_retrieve_cliente_unauthenticated(self):
        """Test para obtener un cliente sin autenticación"""
        self.client.force_authenticate(user=None)  # Eliminar autenticación
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_cliente_authenticated(self):
        """Test para actualizar un cliente con usuario autenticado"""
        data = {
            "nombre": "Juan Carlos",
            "apellido": "Pérez",
            "documento": "12345678",
            "email": "juan.carlos.perez@example.com",
            "direccion": "Calle Nueva 123",
            "telefono": "987654321",
            "estado": False,
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Cliente editado exitosamente")

    def test_update_cliente_unauthenticated(self):
        """Test para actualizar un cliente sin autenticación"""
        self.client.force_authenticate(user=None)  # Eliminar autenticación
        data = {
            "nombre": "Juan Carlos",
            "apellido": "Pérez",
            "documento": "12345678",
            "email": "juan.carlos.perez@example.com",
            "direccion": "Calle Nueva 123",
            "telefono": "987654321",
            "estado": False,
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_cliente_authenticated(self):
        """Test para eliminar un cliente con usuario autenticado"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_cliente_unauthenticated(self):
        """Test para eliminar un cliente sin autenticación"""
        self.client.force_authenticate(user=None)  # Eliminar autenticación
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
