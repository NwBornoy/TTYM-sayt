from django.contrib import admin, messages
from django.utils import timezone

from .models import TelegramUser, SupportMessage, Broadcast, AdminNotification
from .services import send_telegram_message, broadcast


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ("text", "is_sent", "sent_count", "failed_count", "created_at")
    readonly_fields = ("is_sent", "sent_count", "failed_count")
    actions = ["send_now"]

    @admin.action(description="Tanlangan xabarlarni hammaga yuborish")
    def send_now(self, request, queryset):
        for b in queryset.filter(is_sent=False):
            ok, fail = broadcast(b.text)
            b.is_sent, b.sent_count, b.failed_count = True, ok, fail
            b.save()
            self.message_user(
                request,
                f"«{b.text[:30]}»: yetkazildi {ok}, xato {fail}",
                messages.SUCCESS,
            )


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "username", "chat_id", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("full_name", "username", "chat_id")


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ("tg_user", "text", "is_answered", "created_at")
    list_filter = ("is_answered", "created_at")
    search_fields = ("text", "tg_user__full_name")
    fields = ("tg_user", "text", "created_at", "reply_text", "reply_sent", "replied_at")
    readonly_fields = ("tg_user", "text", "created_at", "reply_sent", "replied_at")

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        if obj.reply_text and not obj.reply_sent:
            ok = send_telegram_message(
                obj.tg_user.chat_id, f"👨‍⚕️ Admin javobi:\n{obj.reply_text}"
            )
            if ok:
                obj.reply_sent = True
                obj.is_answered = True
                obj.replied_at = timezone.now()
                messages.success(request, "Javob Telegramga yuborildi ✅")
            else:
                messages.error(
                    request,
                    "Yuborib bo'lmadi. Foydalanuvchi botni bloklagan bo'lishi mumkin.",
                )
        super().save_model(request, obj, form, change)


@admin.action(description="O'qilgan deb belgilash")
def mark_read(modeladmin, request, queryset):
    queryset.update(is_read=True)


@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ("text", "is_read", "created_at")
    list_filter = ("is_read",)
    actions = [mark_read]