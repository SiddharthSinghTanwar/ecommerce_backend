# authentication/utils.py
import random
from django.utils import timezone
from datetime import timedelta

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def is_otp_valid(user):
    return user.otp_valid_until and user.otp_valid_until > timezone.now()

# authentication/views.py
from django.contrib.auth import get_user_model
from .utils import generate_otp, is_otp_valid

User = get_user_model()

class RequestOTPView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        phone_number = request.data.get('phone_number')
        try:
            user = User.objects.get(phone_number=phone_number)
            otp = generate_otp()
            user.otp = otp
            user.otp_valid_until = timezone.now() + timedelta(minutes=10)
            user.save()
            # In a real-world scenario, you would send the OTP via SMS here
            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        try:
            user = User.objects.get(phone_number=phone_number, otp=otp)
            if is_otp_valid(user):
                login(request, user)
                user.otp = None
                user.otp_valid_until = None
                user.save()
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Update authentication/urls.py to include these new views
urlpatterns += [
    path('request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
]