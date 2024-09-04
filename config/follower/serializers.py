from rest_framework import serializers
from .models import Follower, Notification
from djoser.serializers import UserSerializer



class FollowerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['id', 'follower', 'followed']



class NotificationsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        