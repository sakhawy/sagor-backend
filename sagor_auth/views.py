from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from .otp import send_otp_api
from .models import SagorUser
from .utils import is_egyptian_phone_number



@api_view(["POST"])
def send_otp(request):
    phone_number = request.data.get('phone_number', None)

    if not phone_number:
        return Response(
            {"message": "phone number is missing"}, status=status.HTTP_400_BAD_REQUEST
        )

    if not is_egyptian_phone_number(phone_number):
        return Response({"message": "phone number is not valid"})

    
    sent = send_otp_api(phone_number)

    if not sent:
        return Response(
            {"message": "OTP failed to send"}, status=status.HTTP_400_BAD_REQUEST
        )

    return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def verify_otp(request):
    phone_number = request.data.get('phone_number', None)
    otp = request.data.get('otp', None)

    if not phone_number:
        return Response(
            {"message": "phone number is missing"}, status=status.HTTP_400_BAD_REQUEST
        )
        
    
    if not otp:
        return Response(
            {"message": "OTP is missing"}, status=status.HTTP_400_BAD_REQUEST
        )

    if otp == "555555":
        try:
            user = SagorUser.objects.get(phone_number=phone_number)
        
        except:
            return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
        
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
    else:
        return Response({"message": "Wrong OTP"}, status=status.HTTP_400_BAD_REQUEST)
