from rest_framework.serializers import ModelSerializer

from ..models import Notification


class NotificationWrite(
    ModelSerializer["Notification"],
):
    class Meta:
        model = Notification

        fields = ("starred",)
