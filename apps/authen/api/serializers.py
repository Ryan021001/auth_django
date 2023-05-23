from rest_framework import serializers


class LoginRequest(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)


class UserLoginInfo(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()


class LoginResponse(serializers.Serializer):
    access_token = serializers.CharField()
    token_type = serializers.CharField(default='Bearer')
    user = UserLoginInfo(required=True)
