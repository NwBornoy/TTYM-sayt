from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from .models import (
    NewUserNotification,
    Notification, Post, News, Gallery, AboutMedia, EkoActivity,
    Leader, StaffMember, Law, PresidentialDecree, GovernmentDecree,
    NormativeDocument, FinancialTransparencyDocument, HRPolicyDocument,
    OrganizationalLegalInfo, ActivityResultsInfo, AntiCorruptionPost,
)

User = get_user_model()


@receiver(post_save, sender=User)
def create_new_user_notification(sender, instance, created, **kwargs):
    """Yangi foydalanuvchi ro'yxatdan o'tganda avtomatik bildirishnoma yaratadi."""
    if created:
        NewUserNotification.objects.create(user=instance)


# =========================================================
# UMUMIY BILDIRISHNOMALAR (sayt kontenti uchun)
# =========================================================

NOTIF_MODELS = {
    Post: ("Yangi maqola", "📰"),
    News: ("Yangi yangilik", "📢"),
    Gallery: ("Yangi galereya", "🖼️"),
    AboutMedia: ("Markazimizdan yangi lavha", "🖼️"),
    EkoActivity: ("Yangi ekofaol xodim", "🌱"),
    Leader: ("Yangi rahbar", "👤"),
    StaffMember: ("Markaziy apparatga yangi xodim", "🧑‍💼"),
    Law: ("Yangi qonun", "⚖️"),
    PresidentialDecree: ("Yangi prezident hujjati", "📜"),
    GovernmentDecree: ("Yangi hukumat hujjati", "📋"),
    NormativeDocument: ("Yangi normativ hujjat", "📄"),
    FinancialTransparencyDocument: ("Yangi moliya hujjati", "💰"),
    HRPolicyDocument: ("Yangi kadrlar siyosati hujjati", "🧑‍💼"),
    OrganizationalLegalInfo: ("Yangi tashkiliy-huquqiy ma'lumot", "🏛️"),
    ActivityResultsInfo: ("Yangi faoliyat natijalari", "📊"),
    AntiCorruptionPost: ("Yangi korrupsiyaga qarshi post", "🚫"),
}


def make_handler(label, icon):
    def handler(sender, instance, created, **kwargs):
        if not created:
            return
        if hasattr(instance, "is_published") and not instance.is_published:
            return
        Notification.objects.create(
            content_type=ContentType.objects.get_for_model(sender),
            object_id=instance.pk,
            title=f"{label}: {str(instance)[:80]}",
            icon=icon,
        )
    return handler


for model, (label, icon) in NOTIF_MODELS.items():
    post_save.connect(make_handler(label, icon), sender=model)