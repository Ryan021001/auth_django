from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from apps.user.api.serializers import UserResponse
from rest_framework.response import Response
from rest_framework import status

from apps.user.models import User, UserManager
from auth_django.decorators import roles
from common.constants import RolesEnum
from rest_framework.decorators import action


@extend_schema(tags=["User"])
class UserApiView(viewsets.ModelViewSet):
    # authentication_classes = []
    # permission_classes = []

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserResponse

    # @action(detail=False, methods=["post"])
    @roles(allowed_roles=["admin"])
    def perform_create(self, serializer):
        password = self.request.data.get("password")
        if password:
            user = serializer.save()
            user.set_password(password)
            user.save()

    # @roles(allowed_roles=["user"])
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
