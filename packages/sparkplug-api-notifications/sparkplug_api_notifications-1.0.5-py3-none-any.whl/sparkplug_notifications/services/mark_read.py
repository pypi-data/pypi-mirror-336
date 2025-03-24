from ..models.notification import Notification


def mark_read(uuids: list[str]) -> None:
    qs = Notification.objects.filter(uuid__in=uuids)
    qs.update(read=True)
