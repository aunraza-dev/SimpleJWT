from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('resetPasswordOTP/', ResetPasswordOTPView.as_view(), name='reset-password'),
    path('otpVerified/', OtpVerifiedView.as_view(), name='otp-verified'),
    path('changePassword/', ChangePasswordView.as_view(), name='change-password'),
    path('plans/', PlanListCreateAPIView.as_view(), name='plan-list-create'),
    path('plans/<int:pk>/', PlanRetrieveUpdateDestroyAPIView.as_view(), name='plan-detail'),
    path('features/', FeatureListCreateAPIView.as_view(), name='feature-list-create'),
    path('features/<int:pk>/', FeatureRetrieveUpdateDestroyAPIView.as_view(), name='feature-detail'),
    path('contactUs/', ContactUsAPIView.as_view(), name='contact-us'),
    path('buyPackage/', BuyPackageAPIView.as_view(), name='buy-package'),
]
