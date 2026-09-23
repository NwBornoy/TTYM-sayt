from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import NewUserNotification

User = get_user_model()


@receiver(post_save, sender=User)
def create_new_user_notification(sender, instance, created, **kwargs):
    """Yangi foydalanuvchi ro'yxatdan o'tganda avtomatik bildirishnoma yaratadi."""
    if created:
        NewUserNotification.objects.create(user=instance)