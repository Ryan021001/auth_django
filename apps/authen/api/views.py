from uuid import uuid4
from datetime import timedelta
from django.core.cache import cache
import random

from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from auth_django.decorators import roles
from common.auth import User
from common.constants import RolesEnum

from common.exceptions import BadRequest, Unauthorized, InternalServerError
from common.jwt_manager import JWTManager
from common.serializers import ErrorResponse
from common.throttling import UserLoginRateThrottle
from common.utils import send_custom_email
from .serializers import (
    ForgotPassRequest,
    ForgotPassResponse,
    LoginRequest,
    LoginResponse,
    LogoutResponse,
    RefreshRequest,
    RefreshResponse,
    ResetPassRequest,
    ResetPassResponse,
    VertifyCodeRequest,
    VertifyCodeResponse,
)


class GenerateToken:
    @staticmethod
    def _create_token(user, refresh=True):
        expired = timezone.localtime(timezone.now()) + timedelta(
            hours=settings.JWT_TOKEN_EXPIRE_HOURS
        )
        payload = {"jti": uuid4().hex, "sub": str(user.id), "exp": expired}
        token = JWTManager.create_token(payload, secret_key=settings.SECRET_KEY)

        if refresh:
            expired = timezone.localtime(timezone.now()) + timedelta(
                hours=settings.REFRESH_JWT_TOKEN_EXPIRE_HOURS
            )
            payload = {"jti": uuid4().hex, "sub": str(user.id), "exp": expired}
            re_token = JWTManager.create_token(payload, secret_key=settings.SECRET_KEY)

            User.objects.update_or_create(
                id=user.id,
                defaults={
                    "re_token": re_token,
                },
            )

            return {"access_token": token, "refresh_token": re_token}

        return token


class GenerateCode:
    @staticmethod
    def _set_key_forgot_password(userId, securityCode):
        key = f"user{userId}"
        keyValue = cache.get(key)
        if keyValue:
            raise BadRequest(400000, error_message=_("Please enter the code"))
        else:
            cache.set(key, securityCode, timeout=3600)

        return

    @staticmethod
    def _verify_security_code(userId, securityCode):
        key = f"user{userId}"
        data = cache.get(key)
        if data:
            if data != securityCode:
                raise BadRequest(400000, error_message=_("Code is invalid!"))
            cache.set(key, securityCode, timeout=36000)
            return

        else:
            raise BadRequest(400000, error_message=_("The code has expired!"))


@extend_schema(tags=["Authentication"])
class ForgotPassAPIView(APIView, GenerateCode):
    permission_classes = []
    authentication_classes = []

    @extend_schema(
        request=ForgotPassRequest,
        responses={200: ForgotPassResponse, 400: ErrorResponse, 500: ErrorResponse},
    )
    # @roles(allowed_roles=["admin"])
    def post(self, request):
        serializer = ForgotPassRequest(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(400000, error_detail=serializer.errors)

        email = serializer.validated_data.get("email")
        user = User.objects.filter(email=email, is_active=True).first()
        if not user:
            raise Unauthorized(401000, error_message=_("Email or user is not exits"))
        code = "".join(random.choices("0123456789", k=6))
        self._set_key_forgot_password(user.id, code)

        try:
            mail_subject = "Code"
            send_custom_email.delay(mail_subject, code, [email])
            response = ForgotPassResponse(
                {"message": "please check your email to take Code"}
            )

            return Response(response.data)

        except:
            raise InternalServerError(500000, error_detail=serializer.errors)


@extend_schema(tags=["Authentication"])
class VertifyCodeAPIView(APIView, GenerateCode):
    permission_classes = []
    authentication_classes = []

    @extend_schema(
        auth=[],
        request=VertifyCodeRequest,
        responses={200: VertifyCodeResponse, 400: ErrorResponse, 500: ErrorResponse},
    )
    def post(self, request):
        serializer = VertifyCodeRequest(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(400000, error_detail=serializer.errors)

        email = serializer.validated_data.get("email")
        code = serializer.validated_data.get("code")
        user = User.objects.filter(email=email, is_active=True).first()
        if not user:
            raise Unauthorized(401000, error_message=_("Email or user is not exits"))
        self._verify_security_code(user.id, code)
        response = ForgotPassResponse({"message": "Vertify code successfully"})
        return Response(response.data)


@extend_schema(tags=["Authentication"])
class ResetPassAPIView(APIView, GenerateCode):
    permission_classes = []
    authentication_classes = []

    @extend_schema(
        request=ResetPassRequest,
        responses={200: ResetPassResponse, 400: ErrorResponse, 500: ErrorResponse},
    )
    def post(self, request):
        serializer = ResetPassRequest(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(400000, error_detail=serializer.errors)

        email = serializer.validated_data.get("email")
        new_pass = serializer.validated_data.get("new_pass")
        code = serializer.validated_data.get("code")

        user = User.objects.filter(email=email, is_active=True).first()
        if not user:
            raise Unauthorized(401000, error_message=_("Email or user is not exits"))
        self._verify_security_code(user.id, code)
        cache.delete(f"user{user.id}")

        user.set_password(new_pass)
        user.save()

        response = ForgotPassResponse({"message": "Reset password successfully"})
        return Response(response.data)


@extend_schema(tags=["Authentication"])
class LoginAPIView(APIView, GenerateToken):
    permission_classes = []
    authentication_classes = []
    throttle_classes = [UserLoginRateThrottle]

    @extend_schema(
        auth=[],
        request=LoginRequest,
        responses={200: LoginResponse, 400: ErrorResponse, 500: ErrorResponse},
    )
    def post(self, request):
        serializer = LoginRequest(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(400000, error_detail=serializer.errors)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = User.objects.filter(username=username).first()
        if not user or (user and not check_password(password, user.password)):
            raise Unauthorized(
                401000, error_message=_("The username or password is incorrect.")
            )

        token = self._create_token(user)
        response = LoginResponse({**token, "user": user})
        return Response(response.data)


@extend_schema(tags=["Authentication"])
class LogoutAPIView(APIView, GenerateToken):
    @extend_schema(
        responses={200: LogoutResponse, 400: ErrorResponse, 500: ErrorResponse},
    )
    def patch(self, request):
        userId = request.user.id
        user = User.objects.filter(id=userId).first()
        if not user:
            raise Unauthorized(401000, error_message=_("The user is not exits."))
        user.re_token = ""
        user.save()
        response = LogoutResponse({"message": "Reset password successfully"})
        return Response(response.data)


@extend_schema(tags=["Authentication"])
class RefreshAPIView(APIView, GenerateToken):
    permission_classes = []
    authentication_classes = []

    @extend_schema(
        auth=[],
        request=RefreshRequest,
        responses={200: RefreshRequest, 400: ErrorResponse, 500: ErrorResponse},
    )
    def post(self, request):
        serializer = RefreshRequest(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(400000, error_detail=serializer.errors)

        user_id = serializer.validated_data.get("user_id")
        refresh_token = serializer.validated_data.get("refresh_token")

        token = JWTManager.decode_token(refresh_token, secret_key=settings.SECRET_KEY)
        user = User.objects.filter(re_token=refresh_token).first()

        if not user or (user and user.id != user_id):
            raise Unauthorized(401000, error_message=_("The user is not exits."))

        token = self._create_token(user, False)

        response = RefreshResponse({"access_token": token, "user": user})
        return Response(response.data)
