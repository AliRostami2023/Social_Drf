from rest_framework import serializers
from .models import *
from django.utils.text import slugify



class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'title', 'description', 'image', 'video', 'public']



class PostListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class UpdatePostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'description', 'video', 'image', 'public']

