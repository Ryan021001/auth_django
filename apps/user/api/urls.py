from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.user.api import views


router = DefaultRouter()
router.register("user", views.UserApiView)

urlpatterns = [
    path("", include(router.urls)),
]
