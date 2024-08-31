from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from .serializers import *
from .models import *
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema

class RegisterView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=UserSerializer,
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({
                'data': {},
                'msg': 'Email already exists.',
                'success': False,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'data': {
                    'username': user.username,
                    'email': user.email
                },
                'msg': 'User created successfully.',
                'success': True,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'data': serializer.errors,
            'msg': 'Registration failed.',
            'success': False,
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=LoginSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                'data': serializer.validated_data['token'],
                'msg': 'Login successful.',
                'success': True,
            }, status=status.HTTP_200_OK)
        return Response({
            'data': serializer.errors,
            'msg': 'Invalid Credentials!',
            'success': False,
        }, status=status.HTTP_400_BAD_REQUEST)
    
class ResetPasswordOTPView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=ResetPasswordOTPSerializer,
    )

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordOTPSerializer(data=request.data)
        if serializer.is_valid():
            otp, user = serializer.save()
            return Response({
                'data': {
                    'email': user.email,
                },
                'msg': 'OTP generated and sent to email successfully.',
                'success': True,
            }, status=status.HTTP_200_OK)
        return Response({
            'data': serializer.errors,
            'msg': 'Reset Password Failed.',
            'success': False,
        }, status=status.HTTP_400_BAD_REQUEST)
    
class OtpVerifiedView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=OtpVerifiedSerializer,
    )

    def post(self, request, *args, **kwargs):
        serializer = OtpVerifiedSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'data': {
                    'email': user.email,
                    'otp_verified': True,
                },
                'msg': 'OTP verified successfully.',
                'success': True,
            }, status=status.HTTP_200_OK)
        return Response({
            'data': serializer.errors,
            'msg': 'OTP verification failed.',
            'success': False,
        }, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
            request_body=ChangePasswordSerializer
    )

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'data': {
                    'email': user.email,
                },
                'msg': 'Password changed successfully.',
                'success': True,
            }, status=status.HTTP_200_OK)
        return Response({
            'data': serializer.errors,
            'msg': 'Password change failed.',
            'success': False,
        }, status=status.HTTP_400_BAD_REQUEST)

class PlanListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = serializer.save()
        features = request.data['features']
        feature_serializer = FeatureSerializer(data=features, many=True)
        feature_serializer.is_valid(raise_exception=True)
        features = feature_serializer.save(plan=plan)
        
        return Response(status=status.HTTP_200_OK, data=serializer.data)

class PlanRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        features_id = serializer.data['id']
        features = Feature.objects.filter(id = features_id)
        serializer.data['features'] = features
        return Response(status=status.HTTP_200_OK, data=serializer.data)

class FeatureListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

class FeatureRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView): 
    permission_classes = [AllowAny]
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

class ContactUsAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
            request_body=ContactUsSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            contact_us = serializer.save()
            return Response({
                'data': {
                    'fullName': contact_us.fullName,
                    'email': contact_us.email,
                    'message': contact_us.message,
                },
                'msg': 'Newsletter subscribed successfully.',
                'success': True,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'data': serializer.errors,
            'msg': 'Newsletter Subscription failed.',
            'success': False,
        }, status=status.HTTP_400_BAD_REQUEST)
    
class BuyPackageAPIView(APIView):
    permission_classes= [AllowAny]
    @swagger_auto_schema(
            request_body=BuyPackageSerializer
    )
    def post(self,request, *args, **kwargs):
        serializer = BuyPackageSerializer(data=request.data)
        if serializer.is_valid():
            buy_package=serializer.save()
            return Response({
                'data': {
                    'email': buy_package.email,
                    'message': buy_package.message
                },
                'msg': 'Request to buy Package Succesfull.',
                'success': True,
                }, status=status.HTTP_201_CREATED)
        return Response({
            'data': serializer.errors,
            'msg': 'Request to buy package not Succesfull.',
            'success': False,
        }, status=status.HTTP_400_BAD_REQUEST)