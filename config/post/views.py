from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.permissions import AllowAny
from .permissions import IsAuthorOrReadOnly
from django.db.models import Q


class PostListCreateApiView(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    http_method_names = ['get', 'post']


    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.select_related('user').filter(
                Q(user=self.request.user) | Q(public=True))
        return Post.objects.select_related('user').published()


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostListSerializers

    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthorOrReadOnly()]
        return [AllowAny()]
    

class UpdatePostViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                            GenericViewSet ):
    serializer_class = UpdatePostSerializers
    http_method_names = ['get', 'put', 'patch', 'delete']


    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.select_related('user').filter(
                Q(user=self.request.user) | Q(public=True))
        return super().get_queryset()


    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthorOrReadOnly()]
        return [AllowAny()]
    