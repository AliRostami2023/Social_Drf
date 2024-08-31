from rest_framework import viewsets
from .serializers import FollowerSerializers
from rest_framework import permissions
from .models import Follower
from rest_framework import status
from rest_framework.response import Response


class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.select_related('follower', 'followed').all()
    serializer_class = FollowerSerializers
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':
            if 'followers' in self.request.query_params:
                return Follower.objects.select_related('follower', 'followed').filter(followed=user)
            elif 'following' in self.request.query_params:
                return Follower.objects.select_related('follower', 'followed').filter(follower=user)
        return super().get_queryset()
    

    def create(self, request, *args, **kwargs):
        follower = request.user
        followed_id = request.data.get('followed')

        if not followed_id:
            return Response({'error': 'The followed user ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            followed_id = int(followed_id)
        except ValueError:
            return Response({'error': 'Invalid followed user ID.'}, status=status.HTTP_400_BAD_REQUEST)

        if follower.id == followed_id:
            return Response({'error': 'you cant follow yourself'}, status.HTTP_400_BAD_REQUEST)
        
        if Follower.objects.filter(follower=follower, followed_id=followed_id).exists():
            return Response({'error': 'you are already following this user'}, status.HTTP_400_BAD_REQUEST)
        
        Follower.objects.create(follower=follower, followed_id=followed_id)
        return Response({'status': 'followed'}, status.HTTP_200_OK)
    

    def destroy(self, request, *args, **kwargs):
        follower = request.user
        followed_id = self.kwargs.get('pk')

        try:
            instance = Follower.objects.get(follower=follower, followed_id=followed_id)
            instance.delete()
            return Response({'status': 'unfollowed'}, status.HTTP_200_OK)
        except Follower.DoesNotExist:
            return Response({'error': 'you are not following this user'}, status.HTTP_400_BAD_REQUEST)
        

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
