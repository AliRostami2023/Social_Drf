from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework import permissions
from rest_framework import mixins
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.decorators import action


User = get_user_model()


class UserRagistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CresteUserSerializers


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Otp sent'}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'], url_path='verify-otp')
    def verify_otp(self, request):
        serializer = VerifyCodeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'user verified successfully.'}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

