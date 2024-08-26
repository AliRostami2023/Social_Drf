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
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'title','slug', 'description',
                   'image', 'video', 'created', 'updated',
                     'public', 'like_count']
        

    def get_like_count(self, obj):
        return obj.post_like.count()


class UpdatePostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'description', 'video', 'image', 'public']
    
    def update(self, instance, validated_data):
        instance.slug = slugify(validated_data.get('title', instance.title))
        instance.save()
        return instance
    

class LikePostSerializers(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = ['id', 'user', 'post', 'created']
    

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']
        