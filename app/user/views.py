from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegistrationSerializer


class RegistrationApiView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
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
        return Response(serializer.errors)
