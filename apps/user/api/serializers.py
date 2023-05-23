from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.user.models import User


class UserResponse(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
