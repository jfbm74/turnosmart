# core/views.py:

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail

from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Grupo, Tramite, Ventanilla
from .serializers import (
    GrupoSerializer,
    TramiteSerializer,
    UserSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    PasswordChangeSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    VentanillaSerializer,
)
from rest_framework.viewsets import ModelViewSet
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin



User = get_user_model()


class UserRegister(APIView):
    permission_classes = [AllowAny]  # Aseguramos la no autenticación del endpoint.

    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={
            201: openapi.Response("User created successfully", UserRegisterSerializer),
            400: "Bad Request",
        },
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = [AllowAny]  # Permite el ingreso sin autenticación

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response("Login Successful"),
            401: "Unauthorized",
            400: "Bad Request",
        },
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = UserSerializer(
                    user
                )  # Serializar la información del usuario
                return Response(
                    {
                        "token": token.key,
                        "user": user_serializer.data,
                        "message": "Login Successful",
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Aseguramos la autenticación del endpoint.

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                "Profile data retrieved successfully", UserSerializer
            ),
            403: "Forbidden",
        }
    )
    def get(self, request):
        user_serializer = UserSerializer(
            request.user
        )  # Serializamos la información del usuario actual
        return Response(user_serializer.data, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Aseguramos la autenticación del endpoint.

    @swagger_auto_schema(responses={200: "Logged out successfully", 403: "Forbidden"})
    def post(self, request):
        request.user.auth_token.delete()  # Eliminamos el token actual del usuario
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )


class UserCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Aseguramos la autenticación del endpoint.

    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={
            201: openapi.Response("User created successfully", UserRegisterSerializer),
            400: "Bad Request",
        },
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para cambiar contraseña
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PasswordChangeSerializer)
    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data["new_password"])
            request.user.save()
            return Response(
                {"message": "Contraseña actualizada exitosamente."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para solicitar recuperación de contraseña
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=PasswordResetRequestSerializer)
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data["email"])
            token = PasswordResetTokenGenerator().make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"http://example.com/reset-password/{uidb64}/{token}"

            send_mail(
                "Recuperación de contraseña",
                f"Use el siguiente enlace para restablecer su contraseña: {reset_url}",
                "noreply@example.com",
                [user.email],
                fail_silently=False,
            )

            return Response(
                {"message": "Se ha enviado un enlace de recuperación a su correo."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para confirmar recuperación de contraseña
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=PasswordResetConfirmSerializer)
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uid = force_str(urlsafe_base64_decode(serializer.validated_data["uidb64"]))
            user = User.objects.get(pk=uid)
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                {"message": "La contraseña ha sido restablecida exitosamente."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GrupoViewSet(viewsets.ModelViewSet):
    """
    API para gestionar grupos de ventanillas.
    """

    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    permission_classes = [IsAuthenticated]




class TramiteViewSet(viewsets.ModelViewSet):
    """
    API para gestionar los trámites.
    """
    queryset = Tramite.objects.all()
    serializer_class = TramiteSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Listar todos los tramites")
    def list(self, request, *args, **kwargs):
       return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea un nuevo tramite",
            request_body=TramiteSerializer,
        responses={status.HTTP_201_CREATED: TramiteSerializer(),status.HTTP_400_BAD_REQUEST: "Errores de validación"}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
            responses={status.HTTP_200_OK: TramiteSerializer(),
            status.HTTP_404_NOT_FOUND: "Tramite not found"}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
         request_body=TramiteSerializer,
          responses={
                status.HTTP_200_OK: TramiteSerializer(),
                status.HTTP_400_BAD_REQUEST: "Errores de validación",
                status.HTTP_404_NOT_FOUND: "Tramite not found"
            },
        operation_description="Actualiza un tramite existente"
    )
    def update(self, request, *args, **kwargs):
       return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
          status.HTTP_204_NO_CONTENT: "Trámite eliminado",
           status.HTTP_404_NOT_FOUND: "Tramite no encontrado"
       },
        operation_description="Eliminar un trámite existente"
     )
    def destroy(self, request, *args, **kwargs):
          return super().destroy(request, *args, **kwargs)


class TramiteViewSet(viewsets.ModelViewSet):
    """
    API para gestionar los trámites.
    """
    queryset = Tramite.objects.all()
    serializer_class = TramiteSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Listar todos los tramites")
    def list(self, request, *args, **kwargs):
       return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea un nuevo tramite",
            request_body=TramiteSerializer,
        responses={status.HTTP_201_CREATED: TramiteSerializer(),status.HTTP_400_BAD_REQUEST: "Errores de validación"}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
            responses={status.HTTP_200_OK: TramiteSerializer(),
            status.HTTP_404_NOT_FOUND: "Tramite not found"}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
         request_body=TramiteSerializer,
          responses={
                status.HTTP_200_OK: TramiteSerializer(),
                status.HTTP_400_BAD_REQUEST: "Errores de validación",
                status.HTTP_404_NOT_FOUND: "Tramite not found"
            },
        operation_description="Actualiza un tramite existente"
    )
    def update(self, request, *args, **kwargs):
       return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
          status.HTTP_204_NO_CONTENT: "Trámite eliminado",
           status.HTTP_404_NOT_FOUND: "Tramite no encontrado"
       },
        operation_description="Eliminar un trámite existente"
     )
    def destroy(self, request, *args, **kwargs):
          return super().destroy(request, *args, **kwargs)
    

class TramiteListView(ListView):
    model = Tramite
    template_name = "core/app-tramite-list-view.html"
    context_object_name = "tramites"

    def get_queryset(self):
        return Tramite.objects.all().prefetch_related(
            "ventanilla_transferencia_frecuente",
            "grupo_transferencia_frecuente"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["ventanillas"] = Ventanilla.objects.all()
        context["grupos"] = Grupo.objects.all()

        for tramite in context["tramites"]:
            # 1) Lista de objetos ventanilla para mostrarlos con sus descripciones
            tramite.ventanilla_transferencia_frecuente_objs = (
                tramite.ventanilla_transferencia_frecuente.all()
            )
            
            # 2) Lista de IDs para el data-* (JSON.parse)
            tramite.ventanilla_transferencia_frecuente_ids = list(
                tramite.ventanilla_transferencia_frecuente.all().values_list('id', flat=True)
            )
            
            # Lo mismo con grupos, si deseas separar
            tramite.grupo_transferencia_frecuente_objs = (
                tramite.grupo_transferencia_frecuente.all()
            )
            tramite.grupo_transferencia_frecuente_ids = list(
                tramite.grupo_transferencia_frecuente.all().values_list('id', flat=True)
            )

        return context


class VentanillaViewSet(ModelViewSet):
    """
    API para gestionar ventanillas individuales.
    """

    queryset = Ventanilla.objects.all()
    serializer_class = VentanillaSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Listar todas las ventanillas")
    def list(self, request, *args, **kwargs):
       return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=VentanillaSerializer,
            responses={status.HTTP_201_CREATED: VentanillaSerializer()},
            operation_description="Crear una nueva ventanilla"
    )
    def create(self, request, *args, **kwargs):
         return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
      responses={status.HTTP_200_OK: VentanillaSerializer()},
       operation_description="Obtener los datos de la ventanilla por su id"
    )
    def retrieve(self, request, *args, **kwargs):
         return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
      request_body=VentanillaSerializer,
          responses={status.HTTP_200_OK: VentanillaSerializer(),
         status.HTTP_404_NOT_FOUND: "Ventanilla not found"},
       operation_description="Actualizar la informacion de la ventanilla por id"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
          responses={
                status.HTTP_204_NO_CONTENT: "Ventanilla eliminada",
                status.HTTP_404_NOT_FOUND: "Ventanilla not found"
            },
       operation_description="Eliminar ventanilla por id"
    )
    def destroy(self, request, *args, **kwargs):
         return super().destroy(request, *args, **kwargs)

class VentanillaListView(LoginRequiredMixin, ListView):
    model = Ventanilla
    template_name = "core/app-ventanilla-list-view.html"
    context_object_name = "ventanillas"