from rest_framework.viewsets import ViewSet, ModelViewSet
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
from follower.views import NotificationsViewSet
from follower.serializers import NotificationsSerializers
from uuid import uuid4



class PostViewSet(ModelViewSet):
    pagination_class = PostPaginations

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.select_related('orginal_post', 'user').filter(
                Q(user=self.request.user) | Q(public=True))
        return Post.objects.select_related('orginal_post', 'user')


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return UpdatePostSerializers
        return PostListSerializers

    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthorOrReadOnly()]
        return [AllowAny()]


class CommentCreateListApiView(generics.ListCreateAPIView):
    serializer_class = CommentSerializers
    queryset = Comment.objects.prefetch_related('parent', 'user', 'post')
    permission_classes = [IsAuthenticated]
    pagination_class = CommentPaginations


    def perform_create(self, serializer):
        comment = serializer.save(user=self.request.user)

        post_author = comment.post.user
        if post_author != self.request.user:
            NotificationsViewSet.perform_create(
                serializer=NotificationsSerializers(data={
                    'recipient': post_author.id,
                    'sender': self.request.user.id,
                    'post': comment.post.id,
                    'notification_type': 'comment',
                })
            )


class CommentDetailUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentUpdateSerializers
    queryset = Comment.objects.all()
    

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthorOrReadOnly()]
        return [IsAuthenticated()]



class LikeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = LikePost.objects.select_related('user', 'post')
    serializer_class = LikePostSerializers
    # lookup_field = 'post_pk'


    @action(detail=True, methods=['post'])
    def like(self, request, post_pk=None):
        post = Post.objects.get(pk=post_pk)
        user = request.user
        if LikePost.objects.filter(user=user, post=post).exists():
            return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
        
        LikePost.objects.create(user=user, post=post)

        post_author = post.user
        if post_author != user:
                serializer = NotificationsSerializers(data={
                    'recipient': post_author.id,
                    'sender': user.id,
                    'post': post.id,
                    'notification_type': 'like',
                }
            )
                if serializer.is_valid():
                    serializers.save()
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Liked'}, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['delete'])
    def unlike(self, request, post_pk=None):
        post = Post.objects.get(pk=post_pk)
        user = request.user
        like = LikePost.objects.filter(user=user, post=post).first()
        if not like:
            return Response({'detail': 'Not liked'}, status=status.HTTP_400_BAD_REQUEST)
        
        like.delete()
        return Response({'detail': 'Unliked'}, status=status.HTTP_204_NO_CONTENT)
        


class RepostViewSet(ModelViewSet):
    serializer_class = RepostSerializers
    queryset = Post.objects.select_related('user', 'orginal_post')
    permission_classes = [IsAuthenticated]


    def create(self, request, post_pk=None):
        sender_id = request.user.id

        try:
            original_post = Post.objects.get(pk=post_pk)
            new_slug = slugify(f"{original_post.slug}-{uuid4()}")
            
            Post.objects.create(
                user=request.user,
                title=original_post.title,
                slug=new_slug,
                description=original_post.description,
                image=original_post.image,
                video=original_post.video,
                orginal_post=original_post,
                is_repost=True
            )

            notifications_data = {
                'recipient': original_post.user.id,
                'sender': sender_id,
                'notification_type': 'share',
                'post': original_post.id,
                'message': f"{request.user.username} reposted your post."
            }

            serializer = NotificationsSerializers(data=notifications_data)
            if serializer.is_valid():
                self.perform_create(serializer)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({'detail': 'Post reposted successfully.'}, status=status.HTTP_201_CREATED)

        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
