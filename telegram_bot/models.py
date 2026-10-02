from django.conf import settings
from django.db import models


class TelegramUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="telegram",
        verbose_name="Sayt foydalanuvchisi",
    )
    chat_id = models.BigIntegerField("Telegram ID", unique=True)
    username = models.CharField("Username", max_length=100, blank=True)
    full_name = models.CharField("Ism", max_length=255, blank=True)
    is_active = models.BooleanField("Faol", default=True)
    created_at = models.DateTimeField("Qo'shilgan vaqt", auto_now_add=True)

    class Meta:
        verbose_name = "Telegram foydalanuvchi"
        verbose_name_plural = "Telegram foydalanuvchilar"

    def __str__(self):
        return f"{self.full_name} ({self.chat_id})"


class SupportMessage(models.Model):
    tg_user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, verbose_name="Foydalanuvchi"
    )
    text = models.TextField("Murojaat")
    is_answered = models.BooleanField("Javob berilgan", default=False)
    created_at = models.DateTimeField("Yuborilgan vaqt", auto_now_add=True)
    reply_text = models.TextField("Sizning javobingiz", blank=True)
    reply_sent = models.BooleanField("Javob yuborilgan", default=False)
    replied_at = models.DateTimeField("Javob vaqti", null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Murojaat"
        verbose_name_plural = "Murojaatlar"

    def __str__(self):
        return self.text[:50]


class Broadcast(models.Model):
    text = models.TextField(
        "Xabar matni",
        help_text="Barcha foydalanuvchilarga yuboriladigan xabar",
    )
    is_sent = models.BooleanField("Yuborilgan", default=False)
    sent_count = models.PositiveIntegerField("Yetkazildi", default=0)
    failed_count = models.PositiveIntegerField("Xato", default=0)
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)

    class Meta:
        verbose_name = "Ommaviy xabar"
        verbose_name_plural = "Ommaviy xabarlar"

    def __str__(self):
        return self.text[:50]


class AdminNotification(models.Model):
    text = models.CharField("Matn", max_length=300)
    is_read = models.BooleanField("O'qilgan", default=False)
    created_at = models.DateTimeField("Vaqti", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Admin bildirishnoma"
        verbose_name_plural = "Admin bildirishnomalar"

    def __str__(self):
        return self.text