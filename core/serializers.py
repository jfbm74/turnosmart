from rest_framework import serializers
from .models import UserProfile # Importamos nuestro modelo de usuario personalizado.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
       model = UserProfile  # Ahora el modelo es UserProfile
       fields = ['id', 'username', 'email', 'first_name', 'last_name', 'cedula', 'foto', 'perfil', 'ventanillas_atencion']

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
       model = UserProfile # Ahora el modelo es UserProfile
       fields = ['username', 'email', 'first_name', 'last_name','password']
       extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
         password = validated_data.pop('password')
         user = UserProfile(**validated_data) # Ahora el modelo es UserProfile
         user.set_password(password)
         user.save()
         return user

class UserLoginSerializer(serializers.Serializer):
   username = serializers.CharField()
   password = serializers.CharField()