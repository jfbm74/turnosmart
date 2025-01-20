# core/test.py:

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Setup inicial para las pruebas
        self.admin_user = User.objects.create_superuser(username='admin', password='123456', email='jfbm74@gmail.com')
        self.test_user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        self.logout_url = reverse('logout')
        self.users_url = reverse('create_user')
        self.password_change_url = reverse('password_change')
        self.password_reset_request_url = reverse('password_reset_request')
        self.password_reset_confirm_url = reverse('password_reset_confirm')


    def test_user_registration(self):
        """Test de registro de un nuevo usuario."""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpassword"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data['message'], "User created successfully")
        self.assertIn("data", response.data)
        self.assertEqual(User.objects.count(), 2)  # Verificar que el usuario fue creado en la base de datos

    def test_user_login(self):
        """Test de login del usuario, obteniendo un token."""
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("user", response.data)
        self.assertEqual(response.data['message'], "Login Successful")
        self.assertIsInstance(response.data['token'], str)
    

    def test_user_login_incorrect_credentials(self):
        """Test de login fallido por credenciales incorrectas."""
        data = {
            "username": "testuser",
            "password": "wrongpassword"
            }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data['message'], "Invalid credentials")
    

    def test_user_profile_view(self):
        """Test para obtener el perfil del usuario mediante un token."""
        data = {
            "username": "testuser",
            "password": "testpassword"
        }

        # Realiza la solicitud de login
        login_response = self.client.post(self.login_url, data, format='json')

        # Extrae el token de la respuesta
        token = login_response.data.get('token', None)

        # Fuerza la autenticación
        user = User.objects.get(username='testuser')
        self.client.force_authenticate(user=user, token=token)

        # Realiza la solicitud al perfil
        response = self.client.get(self.profile_url, format='json')

        # Validaciones
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')

    

    def test_user_profile_view_unauthorized(self):
        """Test de acceso al endpoint de perfil sin token."""
        response = self.client.get(self.profile_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    


    def test_user_logout(self):
        """Test para cerrar sesión y eliminar el token del usuario actual."""
        data = {
            "username": "testuser",
            "password": "testpassword"
        }

        # Realiza la solicitud de login
        login_response = self.client.post(self.login_url, data, format='json')        

        # Extrae el token de la respuesta
        token = login_response.data.get('token', None)

        # Configura las credenciales
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # Realiza la solicitud de logout
        response = self.client.post(self.logout_url, format='json')

        # Validaciones
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data['message'], "Logged out successfully")
        self.assertFalse(Token.objects.filter(key=token).exists())

    


    def test_user_registration_authenticated(self):
        """Test para registrar un usuario autenticado."""
        data = {
            "username": "testuser2",
            "email": "test2@example.com",
            "first_name": "Test2",
            "last_name": "User2",
            "password": "testpassword2"
            }
        login_response = self.client.post(self.login_url, data = {
        "username": "admin",
            "password": "123456"
        }, format='json')
        token = login_response.data['token']
        response = self.client.post(self.users_url, data, HTTP_AUTHORIZATION=f'Token {token}', format='json') # forma correcta de pasar el token
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data['message'], "User created successfully")
        self.assertIn("data", response.data)
        self.assertEqual(User.objects.count(), 2) # Verificamos que el usuario fue creado en la base de datos
    


    def test_user_registration_unauthenticated(self):
        """Test para registrar un usuario sin autenticación, enviando petición al endpoint `/users`."""
        data = {
            "username": "testuser3",
            "email": "test3@example.com",
            "first_name": "Test3",
            "last_name": "User3",
            "password": "testpassword3"
        }
        response = self.client.post(self.users_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Cambiado de 403 a 401



    def test_password_change(self):
        """Test para cambiar la contraseña del usuario autenticado."""
        login_response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpassword"
        }, format='json')

        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        response = self.client.post(self.password_change_url, {
            "current_password": "testpassword",
            "new_password": "newpassword123"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Contraseña actualizada exitosamente.")

        # Verificar que el usuario puede iniciar sesión con la nueva contraseña
        login_response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "newpassword123"
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_password_reset_request(self):
        """Test para solicitar un enlace de recuperación de contraseña."""
        response = self.client.post(self.password_reset_request_url, {
            "email": "test@example.com"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Se ha enviado un enlace de recuperación a su correo.")

    def test_password_reset_confirm(self):
        """Test para confirmar la recuperación de contraseña."""
        user = User.objects.get(email="test@example.com")
        from django.contrib.auth.tokens import PasswordResetTokenGenerator
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes

        token = PasswordResetTokenGenerator().make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        response = self.client.post(self.password_reset_confirm_url, {
            "uidb64": uidb64,
            "token": token,
            "new_password": "newpassword123"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "La contraseña ha sido restablecida exitosamente.")

        # Verificar que el usuario puede iniciar sesión con la nueva contraseña
        login_response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "newpassword123"
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    
