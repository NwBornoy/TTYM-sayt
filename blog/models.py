from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field

class NewUserNotification(models.Model):
    """Yangi ro'yxatdan o'tgan foydalanuvchilar haqida bildirishnoma."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Foydalanuvchi",
    )
    is_seen = models.BooleanField(default=False, verbose_name="Ko'rib chiqildi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatdan o'tgan vaqt")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Yangi foydalanuvchi bildirishnomasi"
        verbose_name_plural = "Yangi ro'yxatdan o'tgan foydalanuvchilar"

    def __str__(self):
        status = "Ko'rilgan" if self.is_seen else "Yangi"
        return f"[{status}] {self.user.username} — {self.created_at:%d.%m.%Y %H:%M}"

class MissionGoal(models.Model):
    """Bizning maqsad va vazifalarimiz — admin paneldan boshqariladi."""
    icon = models.CharField(
        max_length=10,
        verbose_name="Ikonka (emoji)",
        help_text="Masalan: 🎯 👥 ⚕️ 🔬 — emoji klaviaturadan yoki emojipedia.org dan nusxa oling"
    )
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    description = models.TextField(verbose_name="Tavsif")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")

    class Meta:
        verbose_name = "Maqsad va vazifa"
        verbose_name_plural = "Bizning maqsad va vazifalarimiz"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    location = models.CharField(max_length=100, blank=True, verbose_name="Shahar/tuman",
                                 help_text="Masalan: Qarshi shahri")
    text = models.TextField(verbose_name="Fikr matni")
    is_approved = models.BooleanField(default=False, verbose_name="Tasdiqlangan (saytda chiqadi)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan sana")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bemor fikri"
        verbose_name_plural = "Bemorlar fikrlari"

    def __str__(self):
        status = "Tasdiqlangan" if self.is_approved else "Kutilmoqda"
        return f"[{status}] {self.name} — {self.text[:30]}"

class AboutMedia(models.Model):
    MEDIA_TYPE_CHOICES = (
        ('photo', 'Rasm'),
        ('video', 'Video'),
    )

    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='photo', verbose_name="Turi")
    image = models.ImageField(upload_to='about_media/photos/', blank=True, null=True, verbose_name="Rasm",
                               help_text="Faqat 'Rasm' turi tanlansa yuklang")
    video_url = models.URLField(blank=True, null=True, verbose_name="Video havolasi",
                                 help_text="Faqat 'Video' turi tanlansa YouTube havolasini kiriting (masalan: https://www.youtube.com/watch?v=XXXXXXXXXXX)")
    caption = models.CharField(max_length=255, verbose_name="Qisqacha tavsif", help_text="Rasm/video tagida chiqadigan matn")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Markaz fotolavhasi"
        verbose_name_plural = "Markazimizdan lavhalar (Rasm/Video)"

    def __str__(self):
        return f"{self.get_media_type_display()} — {self.caption}"

    @property
    def youtube_embed_url(self):
        """video_url dan YouTube video ID ajratib, embed havolasini qaytaradi (oddiy, youtu.be, embed, va Shorts linklarini qo'llab-quvvatlaydi)"""
        if not self.video_url:
            return None

        import re
        match = re.search(
            r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)([\w-]{11})",
            self.video_url
        )
        if match:
            return f"https://www.youtube.com/embed/{match.group(1)}"
        return None
    
class TeamStat(models.Model):
    icon = models.CharField(max_length=10, verbose_name="Icon (emoji)", help_text="Masalan: 👨‍⚕️ yoki 🚑 (emoji klaviaturadan tanlang)")
    number = models.CharField(max_length=20, verbose_name="Raqam/qiymat", help_text="Masalan: 60–100 yoki 24/7 yoki 100%")
    label = models.CharField(max_length=255, verbose_name="Tavsif")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Jamoa statistikasi"
        verbose_name_plural = "Bizning jamoamiz (statistika)"

    def __str__(self):
        return f"{self.icon} {self.number} — {self.label}"
    
class TimelineEvent(models.Model):
    year = models.CharField(max_length=20, verbose_name="Yil", help_text="Masalan: 2025 yoki 2025 – 2026 yoki Bugungi kun")
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    description = models.TextField(verbose_name="Matn")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami", help_text="Kichik raqam yuqorida chiqadi")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Tarix voqeasi"
        verbose_name_plural = "Markaz tarixi (Timeline)"

    def __str__(self):
        return f"{self.year} — {self.title}"


User = get_user_model()


class News(models.Model):
    """Markaz yangiliklari."""
    title = models.CharField("Sarlavha", max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField("Qisqa tavsifi")
    image = models.ImageField("Rasm", upload_to="news/", null=True, blank=True)
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)
    is_published = models.BooleanField("Chop etilgan", default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:200]
        super().save(*args, **kwargs)


class Gallery(models.Model):
    """Foto va videogalereya."""
    MEDIA_TYPE = (
        ("photo", "Rasm"),
        ("video", "Video"),
    )

    title = models.CharField("Sarlavha", max_length=200)
    media_type = models.CharField("Turi", max_length=10, choices=MEDIA_TYPE)
    image = models.ImageField("Rasm", upload_to="gallery/")
    video_url = models.URLField("Video URL", blank=True, null=True, help_text="YouTube yoki boshqa video linki")
    description = models.TextField("Tavsifi", blank=True)
    order = models.IntegerField("Tartibi", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Galereya"
        verbose_name_plural = "Galereya"

    def __str__(self):
        return self.title


class Branch(models.Model):
    """Respublika va viloyat filialları."""
    slug = models.SlugField(
        "Xarita ID (SVG ID bilan bir xil bo'lishi kerak)",
        max_length=60,
        blank=True,
        default="",
        help_text="Faqat interaktiv xarita uchun kerak. Masalan: qarshi-shahar, koson, kitob..."
    )
    name = models.CharField("Filial nomi", max_length=300)
    region = models.CharField("Viloyat/Shahar", max_length=100)
    phone = models.CharField("Telefon", max_length=20)
    email = models.EmailField("Email", blank=True)
    address = models.TextField("Manzil")
    director_name = models.CharField("Direktori ismi", max_length=200, blank=True)
    director_image = models.ImageField("Direktori rasmi", upload_to="directors/", null=True, blank=True)
    telegram = models.URLField("Telegram havolasi", blank=True)
    instagram = models.URLField("Instagram havolasi", blank=True)
    description = models.TextField("Tavsifi", blank=True)
    is_main = models.BooleanField("Bosh filial", default=False)
    order = models.IntegerField("Tartibi", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Filial"
        verbose_name_plural = "Filiallar"

    def __str__(self):
        return f"{self.name} - {self.region}"


class ContactInfo(models.Model):
    """Aloqa ma'lumotlari."""
    phone = models.CharField("Emergency telefon", max_length=20, default="103")
    phone_office = models.CharField("Qabulxona telefoni", max_length=20, blank=True)
    email = models.EmailField("Email")
    address = models.TextField("Manzil")
    working_hours = models.CharField("Ish vaqti", max_length=100, default="24/7")

    class Meta:
        verbose_name = "Aloqa"
        verbose_name_plural = "Aloqa ma'lumotlari"

    def __str__(self):
        return "Aloqa ma'lumotlari"


class SupportTicket(models.Model):

    STATUS = (
        ("new", "Yangi"),
        ("process", "Jarayonda"),
        ("closed", "Yopilgan"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="support_tickets"
    )

    subject = models.CharField(
        "Mavzu",
        max_length=200,
        default="Savol"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="new"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.subject}"


User = get_user_model()


class SupportMessage(models.Model):

    ticket = models.ForeignKey(
    SupportTicket,
    on_delete=models.CASCADE,
    related_name="messages",
    null=True,
    blank=True,
)

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    is_admin = models.BooleanField(default=False)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.message[:30]


class Post(models.Model):
    """Admin (yoki xodim huquqiga ega foydalanuvchi) tomonidan yozilgan maqola."""

    title = models.CharField("Sarlavha", max_length=200)
    slug = models.SlugField("Slug", max_length=220, unique=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Muallif",
        on_delete=models.PROTECT,   # muallif hisobi o'chirilsa ham maqola qolishi kerak
        related_name="posts",
    )
    image = models.ImageField(
        "Rasm",
        upload_to="posts/",
        null=True,
        blank=True,
        help_text="Maqolalar ro'yxatida va sahifa boshida ko'rsatiladigan sarlavha rasmi.",
    )
    body = CKEditor5Field("Matn", config_name="default")
    is_published = models.BooleanField(
        "Chop etilgan",
        default=True,
        help_text="O'chirilgan bo'lsa, maqola faqat adminlarga ko'rinadi.",
    )
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)
    updated_at = models.DateTimeField("Yangilangan vaqt", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Maqola"
        verbose_name_plural = "Maqolalar"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:200] or "maqola"
            slug = base_slug
            n = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base_slug}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    @property
    def approved_comments(self):
        return self.comments.filter(is_approved=True).order_by("created_at")


class Comment(models.Model):
    """
    Har qanday tashrif buyuruvchi (ro'yxatdan o'tgan yoki mehmon) qoldirishi mumkin bo'lgan izoh.
    Standart holatda moderatsiyadan o'tmagan izohlar saytda ko'rinmaydi (spam va suiiste'moldan himoya).
    """

    post = models.ForeignKey(
        Post, verbose_name="Maqola", on_delete=models.CASCADE,
        related_name="comments", null=True, blank=True,
    )
    activity = models.ForeignKey(
        "EkoActivity", verbose_name="Ekofaol post", on_delete=models.CASCADE,
        related_name="comments", null=True, blank=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Ro'yxatdan o'tgan foydalanuvchi",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comments",
    )
    guest_name = models.CharField(
        "Mehmon ismi",
        max_length=80,
        blank=True,
        help_text="Faqat ro'yxatdan o'tmagan foydalanuvchilar uchun.",
    )
    text = models.TextField("Izoh matni", max_length=2000)
    is_approved = models.BooleanField(
        "Tasdiqlangan",
        default=False,
        help_text="Faqat tasdiqlangan izohlar saytda ko'rinadi.",
    )
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"

    def __str__(self):
        return f"{self.display_name}: {self.text[:40]}"

    @property
    def display_name(self):
        if self.user:
            return self.user.get_full_name() or self.user.username
        return self.guest_name or "Anonim"

    @property
    def is_registered(self):
        return self.user_id is not None
    
class Partner(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/')
    website_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


class UsefulLink(models.Model):
    name = models.CharField(max_length=255)          # masalan: "Ўзбекистон Республикаси Ҳукумат портали"
    logo = models.ImageField(upload_to='useful_links/', blank=True, null=True)
    site_name = models.CharField(max_length=100)      # masalan: "gov.uz"
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name
class ErrorReport(models.Model):
    page_url = models.URLField(max_length=500)
    selected_text = models.TextField(verbose_name="Belgilangan matn")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Foydalanuvchi"
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False, verbose_name="Ko'rib chiqildi")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Xato haqida xabar"
        verbose_name_plural = "Xato haqida xabarlar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.selected_text[:50]} — {self.created_at:%d.%m.%Y %H:%M}"
    

# models.py fayliga, News klassidan keyin (yoki istalgan joyga) QO'SHING:

class EkoActivity(models.Model):
    """Ekofaol xodim - obodonlashtirish va ekologik faoliyat postlari."""
    title = models.CharField("Sarlavha", max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField("Qisqa tavsifi")
    image = models.ImageField("Rasm", upload_to="ekofaol/", null=True, blank=True)
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)
    is_published = models.BooleanField("Chop etilgan", default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Ekofaol post"
        verbose_name_plural = "Ekofaol xodim"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:200]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("eko_detail", kwargs={"slug": self.slug})

    @property
    def approved_comments(self):
        return self.comments.filter(is_approved=True).order_by("created_at")
    
class Leader(models.Model):
    """Markaz rahbariyati."""
    full_name = models.CharField("F.I.Sh.", max_length=200)
    position = models.CharField("Lavozimi", max_length=300)
    phone = models.CharField("Telefon", max_length=20, blank=True)
    reception_day = models.CharField(
        "Qabul kuni/vaqti", max_length=100, blank=True,
        help_text="Masalan: Chorshanba 14:00-16:00",
    )
    email = models.EmailField("Email", blank=True)
    photo = models.ImageField("Rasm", upload_to="leaders/", null=True, blank=True)
    order = models.PositiveIntegerField("Tartibi", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Rahbar"
        verbose_name_plural = "Rahbariyat"

    def __str__(self):
        return self.full_name
    

class StaffMember(models.Model):
    """Markaziy apparat xodimlari."""
    full_name = models.CharField("F.I.Sh.", max_length=200)
    position = models.CharField("Lavozimi", max_length=300)
    phone = models.CharField("Telefon", max_length=20, blank=True)
    reception_day = models.CharField(
        "Qabul kuni/vaqti", max_length=100, blank=True,
        help_text="Masalan: Chorshanba 14:00-16:00",
    )
    email = models.EmailField("Email", blank=True)
    photo = models.ImageField("Rasm", upload_to="staff/", null=True, blank=True)
    order = models.PositiveIntegerField("Tartibi", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Xodim"
        verbose_name_plural = "Markaziy apparat"

    def __str__(self):
        return self.full_name

class AntiCorruptionPost(models.Model):
    """Korrupsiyaga qarshi kurashish bo'limidagi mavzular."""
    title = models.CharField("Sarlavha", max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    body = CKEditor5Field("Matn", config_name="default")
    order = models.PositiveIntegerField("Tartibi", default=0)
    is_published = models.BooleanField("Chop etilgan", default=True)
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Korrupsiyaga qarshi kurashish mavzusi"
        verbose_name_plural = "Korrupsiyaga qarshi kurashish"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:200] or "mavzu"
            slug = base_slug
            n = 1
            while AntiCorruptionPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base_slug}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("anticorruption_detail", kwargs={"slug": self.slug})
    
class Law(models.Model):
    """Qonunlar ro'yxati - tashqi havolaga yo'naltiruvchi kartalar."""
    title = models.CharField("Sarlavha", max_length=300)
    description = models.TextField("Qisqa tavsifi")
    image = models.ImageField("Rasm", upload_to="laws/", null=True, blank=True)
    url = models.URLField("Havola (qonun matni joylashgan sahifa)")
    order = models.PositiveIntegerField("Tartibi", default=0)
    is_published = models.BooleanField("Chop etilgan", default=True)
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Qonun"
        verbose_name_plural = "Qonunlar"

    def __str__(self):
        return self.title
    
class PresidentialDecree(models.Model):
    """Prezident farmon, qaror va farmoyishlari - tashqi havolaga yo'naltiruvchi kartalar."""
    title = models.CharField("Sarlavha", max_length=300)
    description = models.TextField("Qisqa tavsifi")
    image = models.ImageField("Rasm", upload_to="decrees/", null=True, blank=True)
    url = models.URLField("Havola (hujjat matni joylashgan sahifa)")
    order = models.PositiveIntegerField("Tartibi", default=0)
    is_published = models.BooleanField("Chop etilgan", default=True)
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Prezident hujjati"
        verbose_name_plural = "Prezident farmon, qaror va farmoyishlari"

    def __str__(self):
        return self.title
class GovernmentDecree(models.Model):
    """Hukumat qarori va farmoyishlari - tashqi havolaga yo'naltiruvchi kartalar."""
    title = models.CharField("Sarlavha", max_length=300)
    description = models.TextField("Qisqa tavsifi")
    image = models.ImageField("Rasm", upload_to="gov_decrees/", null=True, blank=True)
    url = models.URLField("Havola (hujjat matni joylashgan sahifa)")
    order = models.PositiveIntegerField("Tartibi", default=0)
    is_published = models.BooleanField("Chop etilgan", default=True)
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Hukumat hujjati"
        verbose_name_plural = "Hukumat qarori va farmoyishlari"

    def __str__(self):
        return self.title
    
class NormativeDocument(models.Model):
    """Markaz normativ hujjatlari - havola yoki yuklangan faylga yo'naltiruvchi kartalar."""
    title = models.CharField("Sarlavha", max_length=300)
    description = models.TextField("Qisqa tavsifi")
    image = models.ImageField("Rasm (karta uchun)", upload_to="normative/", null=True, blank=True)
    url = models.URLField(
        "Tashqi havola", blank=True,
        help_text="Agar hujjat boshqa saytda joylashgan bo'lsa, shu yerga havolani kiriting.",
    )
    file = models.FileField(
        "Fayl (PDF, Word, Excel, TXT, rasm)", upload_to="normative_files/", null=True, blank=True,
        help_text="Agar hujjat faylini saytga yuklamoqchi bo'lsangiz, shu yerdan tanlang.",
    )
    order = models.PositiveIntegerField("Tartibi", default=0)
    is_published = models.BooleanField("Chop etilgan", default=True)
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Normativ hujjat"
        verbose_name_plural = "Markaz normativ hujjatlari"

    def __str__(self):
        return self.title

    @property
    def link(self):
        """Fayl bo'lsa faylga, aks holda tashqi havolaga yo'naltiradi."""
        if self.file:
            return self.file.url
        return self.url

    @property
    def opens_in_new_tab(self):
        return True

class FinancialTransparencyDocument(models.Model):
    """Moliya-xo'jalik shaffofligi - havola yoki yuklangan faylga yo'naltiruvchi kartalar."""
    title = models.CharField("Sarlavha", max_length=300)
    description = models.TextField("Qisqa tavsifi")
    image = models.ImageField("Rasm (karta uchun)", upload_to="finance_docs/", null=True, blank=True)
    url = models.URLField(
        "Tashqi havola", blank=True,
        help_text="Agar hujjat boshqa saytda joylashgan bo'lsa, shu yerga havolani kiriting.",
    )
    file = models.FileField(
        "Fayl (PDF, Word, Excel, TXT, rasm)", upload_to="finance_files/", null=True, blank=True,
        help_text="Agar hujjat faylini saytga yuklamoqchi bo'lsangiz, shu yerdan tanlang.",
    )
    order = models.PositiveIntegerField("Tartibi", default=0)
    is_published = models.BooleanField("Chop etilgan", default=True)
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Moliya-xo'jalik hujjati"
        verbose_name_plural = "Moliya-xo'jalik shaffofligi"

    def __str__(self):
        return self.title

    @property
    def link(self):
        if self.file:
            return self.file.url
        return self.url


class HRPolicyDocument(models.Model):
    """Kadrlar siyosati - havola yoki yuklangan faylga yo'naltiruvchi kartalar."""
    title = models.CharField("Sarlavha", max_length=300)
    description = models.TextField("Qisqa tavsifi")
    image = models.ImageField("Rasm (karta uchun)", upload_to="hr_docs/", null=True, blank=True)
    url = models.URLField(
        "Tashqi havola", blank=True,
        help_text="Agar hujjat boshqa saytda joylashgan bo'lsa, shu yerga havolani kiriting.",
    )
    file = models.FileField(
        "Fayl (PDF, Word, Excel, TXT, rasm)", upload_to="hr_files/", null=True, blank=True,
        help_text="Agar hujjat faylini saytga yuklamoqchi bo'lsangiz, shu yerdan tanlang.",
    )
    order = models.PositiveIntegerField("Tartibi", default=0)
    is_published = models.BooleanField("Chop etilgan", default=True)
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Kadrlar siyosati hujjati"
        verbose_name_plural = "Kadrlar siyosati"

    def __str__(self):
        return self.title

    @property
    def link(self):
        if self.file:
            return self.file.url
        return self.url
    
class OrganizationalLegalInfo(models.Model):
    """Tashkiliy-huquqiy ma'lumotlar - havola yoki yuklangan faylga yo'naltiruvchi kartalar."""
    title = models.CharField("Sarlavha", max_length=300)
    description = models.TextField("Qisqa tavsifi")
    image = models.ImageField("Rasm (karta uchun)", upload_to="org_legal/", null=True, blank=True)
    url = models.URLField(
        "Tashqi havola", blank=True,
        help_text="Agar hujjat boshqa saytda joylashgan bo'lsa, shu yerga havolani kiriting.",
    )
    file = models.FileField(
        "Fayl (PDF, Word, Excel, TXT, rasm)", upload_to="org_legal_files/", null=True, blank=True,
        help_text="Agar hujjat faylini saytga yuklamoqchi bo'lsangiz, shu yerdan tanlang.",
    )
    order = models.PositiveIntegerField("Tartibi", default=0)
    is_published = models.BooleanField("Chop etilgan", default=True)
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Tashkiliy-huquqiy ma'lumot"
        verbose_name_plural = "Tashkiliy-huquqiy ma'lumotlar"

    def __str__(self):
        return self.title

    @property
    def link(self):
        if self.file:
            return self.file.url
        return self.url


class ActivityResultsInfo(models.Model):
    """Faoliyat va natijalar to'g'risidagi axborot - havola yoki yuklangan faylga yo'naltiruvchi kartalar."""
    title = models.CharField("Sarlavha", max_length=300)
    description = models.TextField("Qisqa tavsifi")
    image = models.ImageField("Rasm (karta uchun)", upload_to="activity_results/", null=True, blank=True)
    url = models.URLField(
        "Tashqi havola", blank=True,
        help_text="Agar hujjat boshqa saytda joylashgan bo'lsa, shu yerga havolani kiriting.",
    )
    file = models.FileField(
        "Fayl (PDF, Word, Excel, TXT, rasm)", upload_to="activity_results_files/", null=True, blank=True,
        help_text="Agar hujjat faylini saytga yuklamoqchi bo'lsangiz, shu yerdan tanlang.",
    )
    order = models.PositiveIntegerField("Tartibi", default=0)
    is_published = models.BooleanField("Chop etilgan", default=True)
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Faoliyat va natijalar axboroti"
        verbose_name_plural = "Faoliyat va natijalar to'g'risidagi axborot"

    def __str__(self):
        return self.title

    @property
    def link(self):
        if self.file:
            return self.file.url
        return self.url