from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny


class ProfileListApiView(generics.ListAPIView):
    queryset = ProfileUser.objects.select_related('user').all()
    serializer_class = ListProfileSerializer
    Permission_classes = [AllowAny]


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProfileUser.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

