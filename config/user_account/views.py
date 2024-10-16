from rest_framework.response import Response
from django.urls import reverse
from rest_framework import status
from .serializers import *
from rest_framework import mixins
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.decorators import action


User = get_user_model()


class UserRagistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializers


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Otp sent',
                                  'redirect_url': reverse('auth:verify_code-list'),
                                  'user_id': user.id,
                                    }, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class VerifyCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = VerifyCodeSerializers


    def create(self, request, *args, **kwargs):
        serializer = VerifyCodeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'user verified successfully.'}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class PasswordResetViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = PasswordResetRequestSerializers


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'We are send email reset password'}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



class ConfirmResetPasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = PasswordResetConfirmSerializers


    def create(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Reset password successfully'}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


