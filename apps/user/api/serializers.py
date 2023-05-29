from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.user.models import User


class UserResponse(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]
        extra_kwargs = {
            "password": {"write_only": "true"},
            "re_token": {"write_only": "true"},
        }


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    # def validate(self, attrs):
    #     # Perform custom validation logic here
    #     username = attrs.get("username")
    #     email = attrs.get("email")
    #     password = attrs.get("password")

    #     # Validate the username
    #     if User.objects.filter(username=username).exists():
    #         raise serializers.ValidationError("Username already exists")

    #     # Validate the email
    #     if User.objects.filter(email=email).exists():
    #         raise serializers.ValidationError("Email already exists")

    #     # Add more validation rules as needed

    #     return attrs
