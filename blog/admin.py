from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Post,
    Comment,
    SupportTicket,
    SupportMessage,
    News,
    Gallery,
    Branch,
    ContactInfo,
    EkoActivity,
)
from .models import Partner, UsefulLink
from .models import ErrorReport
from .models import Leader
from .models import StaffMember
from .models import AntiCorruptionPost
from .models import Law
from .models import PresidentialDecree
from .models import GovernmentDecree
from .models import NormativeDocument
from .models import FinancialTransparencyDocument, HRPolicyDocument
from .models import OrganizationalLegalInfo, ActivityResultsInfo


@admin.register(OrganizationalLegalInfo)
class OrganizationalLegalInfoAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_published", "created_at"]
    list_editable = ["order", "is_published"]
    ordering = ["order"]


@admin.register(ActivityResultsInfo)
class ActivityResultsInfoAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_published", "created_at"]
    list_editable = ["order", "is_published"]
    ordering = ["order"]


@admin.register(FinancialTransparencyDocument)
class FinancialTransparencyDocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_published", "created_at"]
    list_editable = ["order", "is_published"]
    ordering = ["order"]


@admin.register(HRPolicyDocument)
class HRPolicyDocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_published", "created_at"]
    list_editable = ["order", "is_published"]
    ordering = ["order"]


@admin.register(NormativeDocument)
class NormativeDocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_published", "created_at"]
    list_editable = ["order", "is_published"]
    ordering = ["order"]


@admin.register(GovernmentDecree)
class GovernmentDecreeAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_published", "created_at"]
    list_editable = ["order", "is_published"]
    ordering = ["order"]


@admin.register(PresidentialDecree)
class PresidentialDecreeAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_published", "created_at"]
    list_editable = ["order", "is_published"]
    ordering = ["order"]


@admin.register(Law)
class LawAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_published", "created_at"]
    list_editable = ["order", "is_published"]
    ordering = ["order"]

@admin.register(AntiCorruptionPost)
class AntiCorruptionPostAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_published", "created_at"]
    list_editable = ["order", "is_published"]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["order"]


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ["full_name", "position", "order"]
    list_editable = ["order"]
    ordering = ["order"]


@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ["full_name", "position", "order"]
    list_editable = ["order"]
    ordering = ["order"]


@admin.register(EkoActivity)
class EkoActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at",)

@admin.register(ErrorReport)
class ErrorReportAdmin(admin.ModelAdmin):
    list_display = ("selected_text_short", "page_url", "user", "created_at", "is_resolved")
    list_filter = ("is_resolved", "created_at")
    search_fields = ("selected_text", "page_url")
    readonly_fields = ("page_url", "selected_text", "user", "ip_address", "created_at")

    def selected_text_short(self, obj):
        return obj.selected_text[:60]
    selected_text_short.short_description = "Matn"

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)


@admin.register(UsefulLink)
class UsefulLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'site_name', 'order')
    list_editable = ('order',)

# =========================================================
# YANGILIKLAR
# =========================================================

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at",)


# =========================================================
# GALEREYA
# =========================================================

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("title", "media_type", "order", "created_at")
    list_filter = ("media_type", "created_at")
    search_fields = ("title", "description")
    ordering = ("order",)


# =========================================================
# FILIALLAR
# =========================================================

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "director_name", "phone", "is_main", "order")
    list_filter = ("is_main", "region")
    search_fields = ("name", "region", "phone", "email", "slug")
    ordering = ("order",)
    prepopulated_fields = {"slug": ("name",)}


# =========================================================
# ALOQA MA'LUMOTLARI
# =========================================================

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("phone", "email", "working_hours")


# =========================================================
# MAQOLALAR
# =========================================================

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "image_preview",
        "is_published",
        "created_at",
    )

    list_filter = (
        "is_published",
        "created_at",
    )

    search_fields = (
        "title",
        "body",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    readonly_fields = (
        "created_at",
        "updated_at",
        "image_preview_large",
    )

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields + ("author",)

        return self.readonly_fields

    @admin.display(description="Rasm")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px; border-radius:4px;" />',
                obj.image.url,
            )
        return "—"

    @admin.display(description="Rasm ko'rinishi")
    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:200px; border-radius:8px;" />',
                obj.image.url,
            )
        return "Rasm yuklanmagan"


# =========================================================
# IZOHLAR
# =========================================================

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        "display_name",
        "post",
        "short_text",
        "is_approved",
        "created_at",
    )

    list_filter = (
        "is_approved",
        "created_at",
    )

    search_fields = (
        "guest_name",
        "text",
        "user__username",
    )

    actions = [
        "approve_comments",
        "reject_comments",
    ]

    @admin.display(description="Izoh")
    def short_text(self, obj):
        return (
            obj.text[:60] + "…"
            if len(obj.text) > 60
            else obj.text
        )

    @admin.action(description="Tanlangan izohlarni tasdiqlash")
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Tanlangan izohlarni rad etish (yashirish)")
    def reject_comments(self, request, queryset):
        queryset.update(is_approved=False)


# =========================================================
# SUPPORT TICKETS
# =========================================================

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user_info",
        "subject",
        "status_badge",
        "message_count",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "subject",
    )

    ordering = (
        "-updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    @admin.display(description="Foydalanuvchi")
    def user_info(self, obj):
        user = obj.user

        full_name = user.get_full_name()

        if full_name:
            return f"👤 {full_name} (@{user.username})"

        return f"👤 @{user.username}"

    @admin.display(description="Holat")
    def status_badge(self, obj):
        status_map = {
            "new": "🟢 Yangi",
            "process": "🟡 Jarayonda",
            "closed": "⚫ Yopilgan",
        }

        return status_map.get(
            obj.status,
            obj.get_status_display()
        )

    @admin.display(description="Xabarlar")
    def message_count(self, obj):
        return obj.messages.count()


# =========================================================
# SUPPORT MESSAGES
# =========================================================

@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):

    list_display = (
        "sender_info",
        "message_type",
        "ticket_info",
        "message_preview",
        "is_read_status",
        "created_at",
    )

    list_filter = (
        "is_admin",
        "is_read",
        "created_at",
    )

    search_fields = (
        "sender__username",
        "sender__first_name",
        "sender__last_name",
        "message",
        "ticket__subject",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )

    @admin.display(description="Kim yozdi")
    def sender_info(self, obj):
        sender = obj.sender

        full_name = sender.get_full_name()

        if full_name:
            return f"👤 {full_name} (@{sender.username})"

        return f"👤 @{sender.username}"


    @admin.display(description="Turi")
    def message_type(self, obj):
        if obj.is_admin:
            return "🟢 ADMIN JAVOBI"

        return "🔵 FOYDALANUVCHI"

    @admin.display(description="Murojaat")
    def ticket_info(self, obj):
        if not obj.ticket:
            return "❌ Ticket yo'q"

        return f"🎫 #{obj.ticket.id} — {obj.ticket.subject}"


    @admin.display(description="Xabar")
    def message_preview(self, obj):
        if not obj.message:
            return "—"

        if len(obj.message) > 80:
            return obj.message[:80] + "…"

        return obj.message

    @admin.display(description="Holat")
    def is_read_status(self, obj):
        if obj.is_read:
            return "✅ O'qilgan"

        return "🔴 O'qilmagan"