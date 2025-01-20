from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer
from rest_framework.permissions import IsAuthenticated

class UserRegister(APIView):
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
    def post(self, request):
         serializer = UserLoginSerializer(data=request.data)
         if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
               token, created = Token.objects.get_or_create(user=user)
               user_serializer = UserSerializer(user) # Serializar la información del usuario
               return Response({
                 'token': token.key,
                  'user': user_serializer.data,
                 'message': 'Login Successful'
                }, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
  permission_classes = [IsAuthenticated] #  Aseguramos la autenticación del endpoint.
  def get(self, request):
        user_serializer = UserSerializer(request.user) # Serializamos la información del usuario actual
        return Response(user_serializer.data, status=status.HTTP_200_OK)

class UserLogoutView(APIView):
  permission_classes = [IsAuthenticated] #  Aseguramos la autenticación del endpoint.
  def post(self, request):
      request.user.auth_token.delete() #Eliminamos el token actual del usuario
      return Response({'message':'Logged out successfully'}, status=status.HTTP_200_OK)


