from django.urls import path

from .views import LoginAPIView

urlpatterns = [
    path("auth/login", LoginAPIView.as_view(), name="auth_login"),
]
