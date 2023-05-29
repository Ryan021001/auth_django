from django.urls import path

from .views import (
    LoginAPIView,
    RefreshAPIView,
    LogoutAPIView,
    ForgotPassAPIView,
    ResetPassAPIView,
    VertifyCodeAPIView,
)

urlpatterns = [
    path("auth/login", LoginAPIView.as_view(), name="auth_login"),
    path("auth/logout", LogoutAPIView.as_view(), name="auth_logout"),
    path("auth/refresh", RefreshAPIView.as_view(), name="auth_refresh"),
    path("auth/forgot-pass", ForgotPassAPIView.as_view(), name="auth_forgot-pass"),
    path("auth/vertify-code", VertifyCodeAPIView.as_view(), name="auth_vertify-code"),
    path("auth/reset-pass", ResetPassAPIView.as_view(), name="auth_reset-pass"),
]
