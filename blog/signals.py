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
# Har bir model uchun: (label lug'ati 4 tilda, ikonka)

NOTIF_MODELS = {
    Post: ({
        "uz": "Yangi maqola", "uz_cyrl": "Янги мақола",
        "ru": "Новая статья", "en": "New article",
    }, "📰"),
    News: ({
        "uz": "Yangi yangilik", "uz_cyrl": "Янги янгилик",
        "ru": "Новая новость", "en": "New news",
    }, "📢"),
    Gallery: ({
        "uz": "Yangi galereya", "uz_cyrl": "Янги галерея",
        "ru": "Новая галерея", "en": "New gallery",
    }, "🖼️"),
    AboutMedia: ({
        "uz": "Markazimizdan yangi lavha", "uz_cyrl": "Марказимиздан янги лавҳа",
        "ru": "Новый материал о нашем центре", "en": "New media from our center",
    }, "🖼️"),
    EkoActivity: ({
        "uz": "Yangi ekofaol xodim", "uz_cyrl": "Янги экофаол ходим",
        "ru": "Новый эко-активный сотрудник", "en": "New eco-active staff member",
    }, "🌱"),
    Leader: ({
        "uz": "Yangi rahbar", "uz_cyrl": "Янги раҳбар",
        "ru": "Новый руководитель", "en": "New leader",
    }, "👤"),
    StaffMember: ({
        "uz": "Markaziy apparatga yangi xodim", "uz_cyrl": "Марказий аппаратга янги ходим",
        "ru": "Новый сотрудник центрального аппарата", "en": "New central staff member",
    }, "🧑‍💼"),
    Law: ({
        "uz": "Yangi qonun", "uz_cyrl": "Янги қонун",
        "ru": "Новый закон", "en": "New law",
    }, "⚖️"),
    PresidentialDecree: ({
        "uz": "Yangi prezident hujjati", "uz_cyrl": "Янги президент ҳужжати",
        "ru": "Новый документ Президента", "en": "New presidential document",
    }, "📜"),
    GovernmentDecree: ({
        "uz": "Yangi hukumat hujjati", "uz_cyrl": "Янги ҳукумат ҳужжати",
        "ru": "Новый документ Правительства", "en": "New government document",
    }, "📋"),
    NormativeDocument: ({
        "uz": "Yangi normativ hujjat", "uz_cyrl": "Янги норматив ҳужжат",
        "ru": "Новый нормативный документ", "en": "New regulatory document",
    }, "📄"),
    FinancialTransparencyDocument: ({
        "uz": "Yangi moliya hujjati", "uz_cyrl": "Янги молия ҳужжати",
        "ru": "Новый финансовый документ", "en": "New financial document",
    }, "💰"),
    HRPolicyDocument: ({
        "uz": "Yangi kadrlar siyosati hujjati", "uz_cyrl": "Янги кадрлар сиёсати ҳужжати",
        "ru": "Новый документ кадровой политики", "en": "New HR policy document",
    }, "🧑‍💼"),
    OrganizationalLegalInfo: ({
        "uz": "Yangi tashkiliy-huquqiy ma'lumot", "uz_cyrl": "Янги ташкилий-ҳуқуқий маълумот",
        "ru": "Новая организационно-правовая информация", "en": "New organizational and legal information",
    }, "🏛️"),
    ActivityResultsInfo: ({
        "uz": "Yangi faoliyat natijalari", "uz_cyrl": "Янги фаолият натижалари",
        "ru": "Новые результаты деятельности", "en": "New activity results",
    }, "📊"),
    AntiCorruptionPost: ({
        "uz": "Yangi korrupsiyaga qarshi post", "uz_cyrl": "Янги коррупцияга қарши пост",
        "ru": "Новый антикоррупционный пост", "en": "New anti-corruption post",
    }, "🚫"),
}

LANGS = ("uz", "uz_cyrl", "ru", "en")


def get_instance_text(instance, lang):
    """
    Instance modeltranslation bilan ro'yxatga olingan bo'lsa
    (masalan News.title_ru), o'sha tildagi qiymatni qaytaradi.
    Bo'lmasa yoki bo'sh bo'lsa, standart str(instance) ga tushadi.
    """
    field_name = f"title_{lang}"
    value = getattr(instance, field_name, None)
    if value:
        return str(value)[:80]
    return str(instance)[:80]


def make_handler(labels, icon):
    def handler(sender, instance, created, **kwargs):
        if not created:
            return
        if hasattr(instance, "is_published") and not instance.is_published:
            return

        notif = Notification(
            content_type=ContentType.objects.get_for_model(sender),
            object_id=instance.pk,
            icon=icon,
        )

        for lang in LANGS:
            label = labels.get(lang, labels["uz"])
            text = get_instance_text(instance, lang)
            setattr(notif, f"title_{lang}", f"{label}: {text}")

        notif.save()

    return handler


for model, (labels, icon) in NOTIF_MODELS.items():
    post_save.connect(make_handler(labels, icon), sender=model, weak=False)