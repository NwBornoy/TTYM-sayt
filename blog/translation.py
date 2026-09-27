from modeltranslation.translator import register, TranslationOptions
from .models import (
    MissionGoal, AboutMedia, TeamStat, TimelineEvent,
    News, Gallery, Branch, ContactInfo, Post,
    EkoActivity, Leader, StaffMember, AntiCorruptionPost,
    Law, PresidentialDecree, GovernmentDecree, NormativeDocument,
    FinancialTransparencyDocument, HRPolicyDocument,
    OrganizationalLegalInfo, ActivityResultsInfo,
)
from .models import Notification

@register(Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(MissionGoal)
class MissionGoalTR(TranslationOptions):
    fields = ('title', 'description')

@register(AboutMedia)
class AboutMediaTR(TranslationOptions):
    fields = ('caption',)

@register(TeamStat)
class TeamStatTR(TranslationOptions):
    fields = ('label',)

@register(TimelineEvent)
class TimelineEventTR(TranslationOptions):
    fields = ('title', 'description')

@register(News)
class NewsTR(TranslationOptions):
    fields = ('title', 'description')

@register(Gallery)
class GalleryTR(TranslationOptions):
    fields = ('title', 'description')

@register(Branch)
class BranchTR(TranslationOptions):
    fields = ('name', 'region', 'address', 'description')
    # director_name TARJIMA QILINMAYDI — bu odam ismi, barcha tilda bir xil bo'lishi kerak

@register(ContactInfo)
class ContactInfoTR(TranslationOptions):
    fields = ('address', 'working_hours')

@register(Post)
class PostTR(TranslationOptions):
    fields = ('title', 'body')

@register(EkoActivity)
class EkoActivityTR(TranslationOptions):
    fields = ('title', 'description')

@register(Leader)
class LeaderTR(TranslationOptions):
    fields = ('position',)
    # full_name TARJIMA QILINMAYDI — ism-familiya

@register(StaffMember)
class StaffMemberTR(TranslationOptions):
    fields = ('position',)

# --- Hujjat/karta modellari (bir xil tuzilishga ega) ---
_DOC_FIELDS = ('title', 'description')

@register(AntiCorruptionPost)
class AntiCorruptionPostTR(TranslationOptions):
    fields = ('title', 'body')

@register(Law)
class LawTR(TranslationOptions):
    fields = _DOC_FIELDS

@register(PresidentialDecree)
class PresidentialDecreeTR(TranslationOptions):
    fields = _DOC_FIELDS

@register(GovernmentDecree)
class GovernmentDecreeTR(TranslationOptions):
    fields = _DOC_FIELDS

@register(NormativeDocument)
class NormativeDocumentTR(TranslationOptions):
    fields = _DOC_FIELDS

@register(FinancialTransparencyDocument)
class FinancialTransparencyDocumentTR(TranslationOptions):
    fields = _DOC_FIELDS

@register(HRPolicyDocument)
class HRPolicyDocumentTR(TranslationOptions):
    fields = _DOC_FIELDS

@register(OrganizationalLegalInfo)
class OrganizationalLegalInfoTR(TranslationOptions):
    fields = _DOC_FIELDS

@register(ActivityResultsInfo)
class ActivityResultsInfoTR(TranslationOptions):
    fields = _DOC_FIELDS