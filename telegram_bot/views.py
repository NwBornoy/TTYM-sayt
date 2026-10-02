import hmac
import json
import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from .models import TelegramUser, SupportMessage, AdminNotification
from .services import send_telegram_message

log = logging.getLogger(__name__)


def handle_update(update):
    """Webhook ham, lokal polling ham shu funksiyani chaqiradi."""
    msg = update.get("message")
    if not msg:
        return

    chat_id = msg["chat"]["id"]
    frm = msg.get("from", {})
    full_name = f'{frm.get("first_name", "")} {frm.get("last_name", "")}'.strip()
    text = msg.get("text")

    is_admin = chat_id in settings.TELEGRAM_ADMIN_IDS

    # Matn bo'lmasa (rasm, lokatsiya va h.k.)
    if not text:
        if not is_admin:
            send_telegram_message(chat_id, "Hozircha faqat matnli xabar qabul qilamiz. Iltimos, yozib yuboring.")
        return

    # ---- ADMIN ----
    if is_admin:
        if text.startswith("/reply"):
            parts = text.split(maxsplit=2)
            if len(parts) < 3 or not parts[1].isdigit():
                send_telegram_message(chat_id, "Format: /reply <chat_id> <matn>")
            else:
                send_telegram_message(int(parts[1]), f"👨‍⚕️ Admin javobi:\n{parts[2]}")
                send_telegram_message(chat_id, "Yuborildi ✅")
        elif text.startswith("/start"):
            send_telegram_message(
                chat_id,
                "Siz admin sifatida ulangansiz.\n"
                "Javob berish: /reply <chat_id> <matn>\n"
                "Ommaviy xabar: admin paneldagi Broadcast bo'limidan.",
            )
        return

    # ---- ODDIY FOYDALANUVCHI ----
    tg_user, _ = TelegramUser.objects.update_or_create(
        chat_id=chat_id,
        defaults={
            "username": frm.get("username", ""),
            "full_name": full_name,
            "is_active": True,
        },
    )

    if text.startswith("/start"):
        AdminNotification.objects.create(text=f"🆕 {full_name} botga /start bosdi")
        send_telegram_message(
            chat_id,
            "Assalomu alaykum! Murojaatingizni shu yerga yozing, adminlarimiz javob beradi.\n\n"
            "🚨 Shoshilinch holatda darhol 103 ga qo'ng'iroq qiling!",
        )
        return

    SupportMessage.objects.create(tg_user=tg_user, text=text)
    AdminNotification.objects.create(text=f"📩 {full_name}: {text[:100]}")
    for admin_id in settings.TELEGRAM_ADMIN_IDS:
        send_telegram_message(
            admin_id,
            f"📩 Yangi murojaat\n👤 {full_name}\n🆔 {chat_id}\n\n{text}\n\n/reply {chat_id} matn",
        )
    send_telegram_message(chat_id, "Murojaatingiz qabul qilindi ✅")


@csrf_exempt
def webhook(request, secret):
    if request.method != "POST" or not hmac.compare_digest(secret, settings.WEBHOOK_SECRET):
        return HttpResponseForbidden()

    try:
        update = json.loads(request.body)
        handle_update(update)
    except Exception:
        log.exception("Telegram update xatosi")
    return HttpResponse("ok")   # har doim 200, aks holda Telegram qayta yuboradi