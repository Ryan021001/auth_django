from functools import wraps
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import api_view
from django.utils.translation import gettext_lazy as _


def roles(allowed_roles=[]):
    def decorator(view_func):
        def wrap(*args, **kwargs):
            # # Assuming 'role' is a field in your user model'

            # role = (
            #     args[1].user.role
            #     if args[1].user.role == "string"
            #     else args[1].context["request"].user.role
            # )

            if args[1].user.role in allowed_roles:
                return view_func(*args, **kwargs)
            else:
                raise PermissionDenied(403000, error_message=_("You dont permission"))

        return wrap

    return decorator
