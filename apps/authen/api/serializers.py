from rest_framework import serializers

from apps.user.models import User


class LoginRequest(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)


class RefreshRequest(serializers.Serializer):
    user_id = serializers.IntegerField()
    refresh_token = serializers.CharField()


class ForgotPassRequest(serializers.Serializer):
    email = serializers.EmailField()


class VertifyCodeRequest(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()


class ResetPassRequest(serializers.Serializer):
    email = serializers.EmailField()
    new_pass = serializers.CharField()
    code = serializers.CharField()


class UserLoginInfo(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()


class LoginResponse(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    token_type = serializers.CharField(default="Bearer")
    user = UserLoginInfo(required=True)


class LogoutResponse(serializers.Serializer):
    message = serializers.CharField()


class RefreshResponse(serializers.Serializer):
    access_token = serializers.CharField()
    token_type = serializers.CharField(default="Bearer")
    user = UserLoginInfo(required=True)


class ForgotPassResponse(serializers.Serializer):
    message = serializers.CharField()


class VertifyCodeResponse(serializers.Serializer):
    message = serializers.CharField()


class ResetPassResponse(serializers.Serializer):
    message = serializers.CharField()
