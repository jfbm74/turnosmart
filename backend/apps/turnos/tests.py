from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from backend.apps.turnos.models import Sala, Turnero, Menu
from django.contrib.auth import get_user_model
from datetime import datetime
from backend.apps.turnos.models import Horario, FranjaHoraria


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


class HorarioAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        self.client.force_authenticate(user=self.user)

        # Crear franja horaria inicial
        self.franja = FranjaHoraria.objects.create(
            hora_inicio="08:00:00", hora_fin="12:00:00", estado=True
        )

        # Crear horario inicial
        self.horario = Horario.objects.create(
            franja_horaria=self.franja,
            lunes=True,
            martes=False,
            miercoles=True,
            jueves=False,
            viernes=True,
            sabado=False,
            domingo=False,
        )

        self.list_url = reverse("horario-list")
        self.detail_url = reverse("horario-detail", args=[self.horario.id])

    def test_list_horarios_authenticated(self):
        """Test para listar horarios con autenticación."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_horarios_unauthenticated(self):
        """Test para listar horarios sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_horario_authenticated(self):
        """Test para crear un horario con autenticación."""
        data = {
            "franja_horaria": self.franja.id,
            "lunes": False,
            "martes": True,
            "miercoles": False,
            "jueves": True,
            "viernes": False,
            "sabado": True,
            "domingo": False,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Horario.objects.count(), 2)

    def test_create_horario_unauthenticated(self):
        """Test para crear un horario sin autenticación."""
        self.client.force_authenticate(user=None)
        data = {
            "franja_horaria": self.franja.id,
            "lunes": False,
            "martes": True,
            "miercoles": False,
            "jueves": True,
            "viernes": False,
            "sabado": True,
            "domingo": False,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_horario_authenticated(self):
        """Test para eliminar un horario con autenticación."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Horario.objects.count(), 0)

    def test_delete_horario_unauthenticated(self):
        """Test para eliminar un horario sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        Horario.objects.all().delete()
        FranjaHoraria.objects.all().delete()
        User.objects.all().delete()


User = get_user_model()


class GenerarHorariosAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        self.client.force_authenticate(user=self.user)

        # Crear franjas horarias y horarios asociados
        self.franja1 = FranjaHoraria.objects.create(
            hora_inicio="08:00:00", hora_fin="12:00:00", estado=True
        )
        self.franja2 = FranjaHoraria.objects.create(
            hora_inicio="14:00:00", hora_fin="18:00:00", estado=True
        )

        self.horario1 = Horario.objects.create(
            franja_horaria=self.franja1, lunes=True, miercoles=True
        )
        self.horario2 = Horario.objects.create(
            franja_horaria=self.franja2, martes=True, jueves=True
        )

        self.generar_url = reverse("generar-horarios")

    def test_generar_horarios_authenticated(self):
        """Test para generar horarios con autenticación."""
        # Forzar que sea lunes para la prueba
        datetime_now_patch = datetime.now()
        dia_actual = datetime_now_patch.strftime("%A").lower()

        response = self.client.get(self.generar_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if dia_actual in ["monday", "wednesday"]:
            self.assertGreaterEqual(len(response.data["horarios_activos"]), 1)
        else:
            self.assertEqual(len(response.data["horarios_activos"]), 0)

    def test_generar_horarios_unauthenticated(self):
        """Test para generar horarios sin autenticación."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.generar_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        Horario.objects.all().delete()
        FranjaHoraria.objects.all().delete()
        User.objects.all().delete()


class TurneroAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        self.client.force_authenticate(user=self.user)

        # Create menu objects
        self.menu1 = Menu.objects.create(
            nombre="Menu General", descripcion="Opciones generales"
        )
        self.menu2 = Menu.objects.create(
            nombre="Menu Laboratorio", descripcion="Opciones de laboratorio"
        )

        # Create turnero object
        self.turnero = Turnero.objects.create(
            nombre="Turnero Principal", ubicacion="Recepción"
        )

        # Set up URLs with correct dynamic routing
        self.associate_url = reverse(
            "turnero-associate-menus", kwargs={"pk": self.turnero.pk}
        )
        self.get_menus_url = reverse(
            "turnero-get-menus", kwargs={"pk": self.turnero.pk}
        )

    def test_associate_menus(self):
        data = {"menu_ids": [self.menu1.id, self.menu2.id]}
        response = self.client.post(self.associate_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.turnero.refresh_from_db()
        self.assertEqual(self.turnero.menus.count(), 2)

    def test_get_menus(self):
        self.turnero.menus.add(self.menu1, self.menu2)
        response = self.client.get(self.get_menus_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def tearDown(self):

        Turnero.objects.all().delete()
        Menu.objects.all().delete()
        User.objects.all().delete()


class SalaAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear un usuario y autenticarlo
        self.user = User.objects.create_user(
            username="admin", password="password", email="admin@example.com"
        )
        self.client.force_authenticate(user=self.user)

        # Crear salas de espera iniciales
        self.sala1 = Sala.objects.create(
            nombre="Sala Principal", descripcion="Sala principal para recepción"
        )
        self.sala2 = Sala.objects.create(
            nombre="Sala Secundaria", descripcion="Sala para laboratorio"
        )

        # Configurar URLs
        self.list_url = reverse("sala-espera-list")

    def test_list_salas(self):
        """Test para listar todas las salas."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_sala(self):
        """Test para crear una sala de espera."""
        data = {"nombre": "Sala Nueva", "descripcion": "Una nueva sala de espera"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sala.objects.count(), 3)

    def test_retrieve_sala(self):
        """Test para obtener una sala específica."""
        detail_url = reverse("sala-espera-detail", kwargs={"pk": self.sala1.id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nombre"], "Sala Principal")

    def test_update_sala(self):
        """Test para actualizar una sala de espera."""
        detail_url = reverse("sala-espera-detail", kwargs={"pk": self.sala1.id})
        data = {"nombre": "Sala Actualizada", "descripcion": "Descripción actualizada"}
        response = self.client.put(detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.sala1.refresh_from_db()
        self.assertEqual(self.sala1.nombre, "Sala Actualizada")

    def test_delete_sala(self):
        """Test para eliminar una sala de espera."""
        detail_url = reverse("sala-espera-detail", kwargs={"pk": self.sala1.id})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Sala.objects.count(), 1)
