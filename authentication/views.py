from django.shortcuts import render


from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .serializers import UserRegisterSerializer, UserLoginSerializer
from .serializers import UserRegisterSerializer, UserLoginSerializer, OTPRequestSerializer, OTPVerifySerializer
from .models import CustomUser
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta

class UserRegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

class RequestOTPView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = OTPRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user:
                otp = get_random_string(length=6, allowed_chars='0123456789')
                user.otp = otp
                user.otp_valid_until = timezone.now() + timedelta(minutes=10)
                user.save()
                # Send OTP via email (implement this part)
                return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = OTPVerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            user = CustomUser.objects.filter(email=email, otp=otp, otp_valid_until__gt=timezone.now()).first()
            if user:
                login(request, user)
                user.otp = None
                user.otp_valid_until = None
                user.save()
                return Response({"message": "OTP verified and login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

def login_view(request):
    return render(request, 'login.html')

