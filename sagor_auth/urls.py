from django.urls import path

from .views import *

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('send-otp/', send_otp, name='send_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]