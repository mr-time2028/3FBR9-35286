from datetime import datetime
from drf_spectacular.utils import extend_schema

from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
)


class RegistrationApiView(APIView):

    @extend_schema(request=RegistrationSerializer)
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data['username']
        password1 = serializer.data['password1']

        if not get_user_model().objects.filter(username=username).exists():
            get_user_model().objects.create_user(
                username=username,
                password=password1,
                is_active=True
            )
            return Response({"success": "User registered successfully."}, status=status.HTTP_200_OK)
        return Response({"detail": "This username already exists."}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(APIView):

    @extend_schema(request=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        username = serializer.data['username']
        password = serializer.data['password']

        try:
            user = get_user_model().objects.get(username=username)
            if not user.check_password(password):
                raise Exception()
        except Exception:
            return Response({"detail": "Incorrect username or password."}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token

            refresh_token.set_exp(lifetime=settings.ACCESS_TOKEN_LIFETIME)
            access_token.set_exp(lifetime=settings.REFRESH_TOKEN_LIFETIME)

            tokens = {"username": username, "refresh": str(refresh_token), "access": str(access_token)}
            user.last_login = datetime.now()
            user.save()
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({"detail": "User is not confirmed."}, status=status.HTTP_403_FORBIDDEN)
