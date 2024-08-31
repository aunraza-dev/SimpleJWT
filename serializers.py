from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import pyotp
from django.core.mail import send_mail
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                data['token'] = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            else:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Both fields are required')
        return data
    
class ResetPasswordOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def create_otp(self):
        totp = pyotp.TOTP(pyotp.random_base32(), digits=5)
        return totp.now()

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        otp = self.create_otp()
        user.first_name = otp
        user.save()
        
        subject = 'Password Reset OTP'
        message = f'OTP is: {otp}'
        from_email = 'raza.aunharaj@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        
        return otp, user

class OtpVerifiedSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=5)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        if user.first_name != otp:
            raise serializers.ValidationError("Invalid OTP.")

        return data

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        user.last_name = 'True'
        user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=5, write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')
        new_password = data.get('new_password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        if user.first_name != otp:
            raise serializers.ValidationError("Password change not allowed. Wrong OTP.")
        return data

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        subject = 'Password Reset'
        message = f'Your account password was reset successfully.'
        from_email = 'raza.aunharaj@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        return user

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Plan
        fields = '__all__'

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'

class BuyPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyPackage
        fields = '__all__'