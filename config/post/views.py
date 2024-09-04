from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework import mixins
from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from .paginations import PostPaginations, CommentPaginations



class PostListCreateApiView(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    http_method_names = ['get', 'post']
    pagination_class = PostPaginations


    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.select_related('user').filter(
                Q(user=self.request.user) | Q(public=True))
        return Post.objects.select_related('user').all()


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


class CommentCreateListApiView(generics.ListCreateAPIView):
    serializer_class = CommentSerializers
    queryset = Comment.objects.prefetch_related('parent', 'user', 'post').all()
    permission_classes = [IsAuthenticated]
    pagination_class = CommentPaginations


class CommentDetailUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentUpdateSerializers
    queryset = Comment.objects.all()
    

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthorOrReadOnly()]
        return [IsAuthenticated()]



class LikeViewSet(ViewSet):
    permission_classes = [IsAuthenticated]


    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        user = request.user
        if LikePost.objects.filter(user=user, post=post).exists():
            return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
        LikePost.objects.create(user=user, post=post)
        return Response({'detail': 'Liked'}, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['delete'])
    def unlike(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        user = request.user
        like = LikePost.objects.filter(user=user, post=post).first()
        if not like:
            return Response({'detail': 'Not liked'}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response({'detail': 'Unliked'}, status=status.HTTP_204_NO_CONTENT)
