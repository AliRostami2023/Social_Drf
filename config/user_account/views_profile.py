from rest_framework import viewsets, mixins
from .models import ProfileUser
from .serializers import ProfileSerializers
from .permissions import OwnerOrReadOnly


class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = ProfileUser.objects.all()
    serializer_class = ProfileSerializers
    permission_classes = [OwnerOrReadOnly]
