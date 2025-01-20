# core/views.py:

from django.utils.encoding import force_str
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer, PasswordChangeSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail



User = get_user_model()

class UserRegister(APIView):
    permission_classes = [AllowAny]  # Aseguramos la no autenticación del endpoint.

    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={
            201: openapi.Response('User created successfully', UserRegisterSerializer),
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User created successfully",
                "data": serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes = [AllowAny]  # Permite el ingreso sin autenticación

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response('Login Successful'),
            401: 'Unauthorized',
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = UserSerializer(user)  # Serializar la información del usuario
                return Response({
                    'token': token.key,
                    'user': user_serializer.data,
                    'message': 'Login Successful'
                }, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Aseguramos la autenticación del endpoint.

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Profile data retrieved successfully', UserSerializer),
            403: 'Forbidden'
        }
    )
    def get(self, request):
        user_serializer = UserSerializer(request.user)  # Serializamos la información del usuario actual
        return Response(user_serializer.data, status=status.HTTP_200_OK)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Aseguramos la autenticación del endpoint.

    @swagger_auto_schema(
        responses={
            200: 'Logged out successfully',
            403: 'Forbidden'
        }
    )
    def post(self, request):
        request.user.auth_token.delete()  # Eliminamos el token actual del usuario
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

class UserCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Aseguramos la autenticación del endpoint.

    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={
            201: openapi.Response('User created successfully', UserRegisterSerializer),
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User created successfully",
                "data": serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para cambiar contraseña
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PasswordChangeSerializer)
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({"message": "Contraseña actualizada exitosamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para solicitar recuperación de contraseña
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=PasswordResetRequestSerializer)
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            token = PasswordResetTokenGenerator().make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"http://example.com/reset-password/{uidb64}/{token}"

            send_mail(
                'Recuperación de contraseña',
                f'Use el siguiente enlace para restablecer su contraseña: {reset_url}',
                'noreply@example.com',
                [user.email],
                fail_silently=False,
            )

            return Response({"message": "Se ha enviado un enlace de recuperación a su correo."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para confirmar recuperación de contraseña
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=PasswordResetConfirmSerializer)
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['uidb64']))
            user = User.objects.get(pk=uid)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "La contraseña ha sido restablecida exitosamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

