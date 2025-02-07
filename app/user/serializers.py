from django.core.validators import RegexValidator

from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, min_length=4)
    password1 = serializers.CharField(max_length=30, min_length=8)
    password2 = serializers.CharField(max_length=30, min_length=8)

    def validate(self, attrs):
        password1 = attrs.get('password1', None)
        password2 = attrs.get('password2', None)

        if password1 != password2:
            raise ValidationError({"detail": "Your passwords didn't match."}, code=status.HTTP_400_BAD_REQUEST)

        return attrs
