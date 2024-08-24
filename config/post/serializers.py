from rest_framework import serializers
from .models import *
from django.utils.text import slugify
from djoser.serializers import UserSerializer



class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'title', 'description', 'image', 'video', 'public']



class PostListSerializers(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'


class UpdatePostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'description', 'video', 'image', 'public']
    
    def update(self, instance, validated_data):
        instance.slug = slugify(validated_data.get('title', instance.title))
        instance.save()
        return instance
    

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']
        