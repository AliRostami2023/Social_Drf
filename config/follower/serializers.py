from rest_framework import serializers
from .models import Follower
from djoser.serializers import UserSerializer



class FollowerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['id', 'follower', 'followed']
