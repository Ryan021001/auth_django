from uuid import uuid4
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from common.auth import User

from common.exceptions import BadRequest, Unauthorized
from common.jwt_manager import JWTManager
from common.serializers import ErrorResponse
from common.throttling import UserLoginRateThrottle
from .serializers import LoginRequest, LoginResponse


@extend_schema(tags=["Authentication"])
class LoginAPIView(APIView):
    permission_classes = []
    authentication_classes = []
    throttle_classes = [UserLoginRateThrottle]

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

            return token, re_token

        return token

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

        access_token = self._create_token(user)
        response = LoginResponse({"access_token": access_token, "user": user})
        return Response(response.data)
