from django.views import View
from rest_framework.request import Request
from sparkplug_core.permissions import (
    ActionPermission,
    IsAuthenticated,
)

from .models import Notification


class IsOwner(IsAuthenticated):
    def has_object_permission(
        self,
        request: Request,
        view: View,  # noqa: ARG002
        obj: Notification,
    ) -> bool:
        return obj.recipient == request.user


class Permissions(
    ActionPermission,
):
    # object permissions
    read_perms = IsOwner
    write_perms = IsOwner
