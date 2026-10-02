from .models import AdminNotification


def telegram_notifications(request):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated or not user.is_staff:
        return {}
    qs = AdminNotification.objects.filter(is_read=False)
    return {
        "tg_notifications_count": qs.count(),
        "tg_notifications": qs[:5],
    }