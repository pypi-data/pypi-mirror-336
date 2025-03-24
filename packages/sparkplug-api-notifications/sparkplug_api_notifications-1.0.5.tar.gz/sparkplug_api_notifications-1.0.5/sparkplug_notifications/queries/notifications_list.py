from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import QuerySet

from ..models import Notification


def notifications_list(
    recipient: type[AbstractBaseUser],
    starred: bool | None = None,
) -> QuerySet["Notification"]:
    qs = Notification.objects.filter(recipient=recipient)

    # Optionally filter by starred.
    if starred:
        qs = qs.filter(starred=starred)

    return (
        qs.order_by("-created")
        .prefetch_related("recipient")
        .prefetch_related("actor")
    )
