import logging
import time

import requests
from django.conf import settings

log = logging.getLogger(__name__)


def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=10)
    except requests.RequestException as e:
        log.warning("Telegram ulanish xatosi (%s): %s", chat_id, e)
        print(f"SEND XATO {chat_id}: {e}")
        return False

    if r.status_code == 200:
        return True

    log.warning("Telegram rad etdi (%s): %s", chat_id, r.text)
    print(f"SEND XATO {chat_id}: {r.status_code} {r.text}")

    # Foydalanuvchi botni bloklagan bo'lsa, keyingi yuborishlardan chiqarib tashlaymiz
    if r.status_code == 403:
        from .models import TelegramUser
        TelegramUser.objects.filter(chat_id=chat_id).update(is_active=False)
    return False


def broadcast(text):
    """Faol foydalanuvchilarning hammasiga yuboradi. (yuborildi, xato) qaytaradi."""
    from .models import TelegramUser

    ok = fail = 0
    for chat_id in TelegramUser.objects.filter(is_active=True).values_list("chat_id", flat=True):
        if send_telegram_message(chat_id, text):
            ok += 1
        else:
            fail += 1
        time.sleep(0.05)   # Telegram limiti: sekundiga ~30 ta xabar
    return ok, fail