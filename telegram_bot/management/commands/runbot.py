import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from telegram_bot.views import handle_update


class Command(BaseCommand):
    help = "Lokal test: polling orqali botni ishga tushirish"

    def handle(self, *args, **options):
        api = f"https://api.telegram.org/bot{settings.BOT_TOKEN}"
        requests.get(f"{api}/deleteWebhook")
        offset = None
        self.stdout.write("Bot ishga tushdi. To'xtatish: Ctrl+C")
        while True:
            try:
                r = requests.get(f"{api}/getUpdates",
                                 params={"timeout": 30, "offset": offset},
                                 timeout=40).json()
            except requests.RequestException:
                continue
            for update in r.get("result", []):
                offset = update["update_id"] + 1
                try:
                    handle_update(update)
                except Exception as e:
                    self.stderr.write(f"Xato: {e}")