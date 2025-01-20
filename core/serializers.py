from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model() # get the custom User model

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'first_name', 'last_name', 'cedula', 'foto', 'perfil', 'ventanillas_atencion']

class UserRegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'email', 'first_name', 'last_name','password']
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
     password = validated_data.pop('password')
     user = User(**validated_data)
     user.set_password(password)
     user.save()
     return user

class UserLoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()