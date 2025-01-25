# core/serializers.py

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import UserProfile, Grupo, Ventanilla


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile  # Ahora el modelo es UserProfile
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "cedula",
            "foto",
            "perfil",
            "ventanillas_atencion",
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile  # Ahora el modelo es UserProfile
        fields = ["username", "email", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = UserProfile(**validated_data)  # Ahora el modelo es UserProfile
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


# Serializer para cambio de contraseña
class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context["request"].user
        if not user.check_password(data["current_password"]):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return data


# Serializer para solicitud de recuperación de contraseña
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No existe un usuario con este correo.")
        return value


# Serializer para establecer una nueva contraseña con token
class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data["uidb64"]))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("El enlace de recuperación es inválido.")

        if not PasswordResetTokenGenerator().check_token(user, data["token"]):
            raise serializers.ValidationError(
                "El token de recuperación no es válido o ha expirado."
            )

        return data


class GrupoSerializer(serializers.ModelSerializer):
     """
        Serializer para el modelo Grupo.
    """
     class Meta:
         model = Grupo
         fields = ['id', 'nombre', 'ventanillas_atencion', 'estado']
         extra_kwargs = {
            'id': {'read_only': True, 'help_text': 'Identificador único del grupo.'},
            'nombre': {'help_text': 'Nombre del grupo'},
            'ventanillas_atencion': {'help_text': 'Lista de ids de ventanillas que pertenecen al grupo.'},
           'estado': {'help_text': 'Estado del grupo'},
         }


class VentanillaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ventanilla
        fields = ['id', 'id_ventanilla', 'descripcion', 'estado']
        extra_kwargs = {
            'id': {'read_only': True},
            'id_ventanilla': {'help_text': 'Identificador único de la ventanilla.'},
            'descripcion': {'help_text': 'Descripción de la ventanilla.'},
            'estado': {'help_text': 'Estado de la ventanilla (activo/inactivo).'},
        }