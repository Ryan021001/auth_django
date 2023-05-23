from django.db import models

from common.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username=username, email=email, password=password)
        user.save()
        return user


class User(AbstractBaseUser, BaseModel):
    username = models.CharField(max_length=31, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    re_token = models.CharField(max_length=255)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_staff:
            return True
        return False

    def has_module_perms(self, app_label):
        if self.is_active and self.is_staff:
            return True
        return False
