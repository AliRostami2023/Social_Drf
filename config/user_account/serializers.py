from djoser.serializers import UserSerializer as BaseUserSerializers, UserCreateSerializer as BaseUserCreateSerializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import ProfileUser


User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializers):
    class Meta(BaseUserCreateSerializers.Meta):
        model = User
        fields = ['full_name', 'email', 'username', 'password']


class UserSerializer(BaseUserSerializers):
    class Meta(BaseUserSerializers.Meta):
        model = User
        fields = '__all__'
        

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = ProfileUser
        fields = ['user', 'avatar', 'about_me', 'gender', 'birthday', 'created']


class ListProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = '__all__'
        