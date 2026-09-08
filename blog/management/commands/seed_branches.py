from django.core.management.base import BaseCommand
from blog.models import Branch


BRANCHES_DATA = [
    {"slug": "qarshi-shahar", "name": "Qarshi shahar filiali", "address": "Qarshi shahri", "is_main": True, "order": 1},
    {"slug": "qarshi-tumani", "name": "Qarshi tumani filiali", "address": "Qarshi tumani", "order": 2},
    {"slug": "shahrisabz-shahar", "name": "Shahrisabz shahar filiali", "address": "Shahrisabz shahri", "order": 3},
    {"slug": "shahrisabz-tumani", "name": "Shahrisabz tumani filiali", "address": "Shahrisabz tumani", "order": 4},
    {"slug": "kitob", "name": "Kitob tumani filiali", "address": "Kitob tumani", "order": 5},
    {"slug": "chiroqchi", "name": "Chiroqchi tumani filiali", "address": "Chiroqchi tumani", "order": 6},
    {"slug": "yakkabog", "name": "Yakkabog\u2018 tumani filiali", "address": "Yakkabog\u2018 tumani", "order": 7},
    {"slug": "qamashi", "name": "Qamashi tumani filiali", "address": "Qamashi tumani", "order": 8},
    {"slug": "guzor", "name": "G\u2018uzor tumani filiali", "address": "G\u2018uzor tumani", "order": 9},
    {"slug": "dehqonobod", "name": "Dehqonobod tumani filiali", "address": "Dehqonobod tumani", "order": 10},
    {"slug": "nishon", "name": "Nishon tumani filiali", "address": "Nishon tumani", "order": 11},
    {"slug": "kasbi", "name": "Kasbi tumani filiali", "address": "Kasbi tumani", "order": 12},
    {"slug": "koson", "name": "Koson tumani filiali", "address": "Koson tumani", "order": 13},
    {"slug": "muborak", "name": "Muborak tumani filiali", "address": "Muborak tumani", "order": 14},
    {"slug": "mirishkor", "name": "Mirishkor tumani filiali", "address": "Mirishkor tumani", "order": 15},
    {"slug": "kokdala", "name": "Ko\u2018kdala tumani filiali", "address": "Ko\u2018kdala tumani", "order": 16},
]


class Command(BaseCommand):
    help = "15 ta Qashqadaryo filialini bazaga avtomatik kiritadi (bo'sh maydonlar bilan)"

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0

        for data in BRANCHES_DATA:
            branch, created = Branch.objects.get_or_create(
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "address": data["address"],
                    "is_main": data.get("is_main", False),
                    "order": data["order"],
                    "director_name": "",
                    "phone": "",
                    "email": "",
                    "telegram": "",
                    "instagram": "",
                },
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  + Yaratildi: {branch.name}"))
            else:
                skipped_count += 1
                self.stdout.write(self.style.WARNING(f"  = O'tkazib yuborildi (allaqachon bor): {branch.name}"))

        self.stdout.write(self.style.SUCCESS(
            f"\nTayyor! {created_count} ta yangi filial yaratildi, {skipped_count} ta o'tkazib yuborildi."
        ))