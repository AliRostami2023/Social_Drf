from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import OtpCode
from .random_code import random_code_otp
from datetime import datetime, timedelta


User = get_user_model()


class CresteUserSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, max_length=10)

    class Meta:
        model = User
        fields = ['phone_number', 'username', 'password', 'confirm_password']


    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('password must be match !')
        return attrs
    

    def create(self, validated_data):
        del validated_data['confirm_password']
        user = User.objects.create_user(**validated_data)

        expired_date = datetime.now() + timedelta(minutes=2)
        OtpCode.objects.create(user=user, code=random_code_otp(), expired_date=expired_date)
        # todo : send sms
        print(f"otp code for {user.username}: {random_code_otp()}")
        return user



class VerifyCodeSerializers(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = ['code', 'expired_date']
        read_only_fields = ['user']
    

    def validate(self, attrs):
        phone_number = attrs.get('user__phone_number')
        code = attrs.get('code')

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError('user not found')
        
        otp = OtpCode.objects.filter(user=user, code=code).first()

        if not otp:
            raise serializers.ValidationError('Invalid otp code !')
                
        if otp.expired_date_over:
            otp.delete_otp
            raise serializers.ValidationError('otp code has expired !')
        
        user.is_active = True
        user.save()

        otp.delete()
        return attrs
