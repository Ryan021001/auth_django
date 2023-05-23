from django.conf import settings
from django.contrib.auth import get_user_model
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.authentication import BaseAuthentication

from common.exceptions import Unauthorized
from common.jwt_manager import JWTManager

AUTH_HEADER_TYPE = (b'Bearer',)
User = get_user_model()


class BearerAuthSchema(OpenApiAuthenticationExtension):
    target_class = 'common.auth.BearerAuthSchema'
    match_subclasses = True
    name = 'Bearer'

    def __init__(self, name=None):
        name = name if name and isinstance(name, str) else BearerAuthSchema.name
        self.name = str(name)
        super().__init__(target=BearerAuthSchema.target_class)

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "Bearer",
            'name': 'Authorization',
        }


class JWTAuth(BaseAuthentication, BearerAuthSchema):

    @staticmethod
    def _get_header(request):
        header = request.META.get('HTTP_AUTHORIZATION')
        if isinstance(header, str):
            header = header.encode(HTTP_HEADER_ENCODING)
        return header

    @staticmethod
    def _get_token(header):
        if not header:
            return None
        parts = header.split()
        if len(parts) == 0:
            return None
        if parts[0] not in AUTH_HEADER_TYPE:
            return None
        if len(parts) != 2:
            return None
        return parts[1]

    def authenticate(self, request):
        header = self._get_header(request)
        token = self._get_token(header)
        if not token:
            return None
        payload = JWTManager.decode_token(token, secret_key=settings.SECRET_KEY)
        user_id = payload.get('sub')

        user = User.objects.filter(id=user_id).first()
        if not user or (user and not user.is_active):
            raise Unauthorized(401003)

        return user, None

    def authenticate_header(self, request):
        return True
