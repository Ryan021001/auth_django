from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from apps.user.api.serializers import UserResponse

from apps.user.models import User


@extend_schema(tags=["User"])
class UserApiView(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserResponse

