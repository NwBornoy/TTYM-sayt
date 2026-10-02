from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import SupportMessage
from .models import Comment
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'location', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'tf-input', 'placeholder': _('Ismingiz')}),
            'location': forms.TextInput(attrs={'class': 'tf-input', 'placeholder': _("Shahar/tuman (ixtiyoriy)")}),
            'text': forms.Textarea(attrs={'class': 'tf-textarea', 'placeholder': _('Fikringizni yozing...'), 'rows': 4}),
        }


class CommentForm(forms.ModelForm):
    guest_name = forms.CharField(
        label=_("Ismingiz"),
        max_length=80,
        required=False,
        help_text=_("Ixtiyoriy — bo'sh qoldirsangiz 'Anonim' deb ko'rsatiladi."),
        widget=forms.TextInput(attrs={"placeholder": _("Ismingiz (ixtiyoriy)")}),
    )
    text = forms.CharField(
        label=_("Izoh"),
        max_length=2000,
        widget=forms.Textarea(attrs={"placeholder": _("Izohingizni yozing…"), "rows": 4}),
    )

    # Honeypot maydoni: oddiy foydalanuvchiga ko'rinmaydi (CSS bilan yashirilgan),
    # lekin avtomatik spam-botlar ko'pincha uni ham to'ldiradi — shu orqali ularni ushlaymiz.
    website = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Comment
        fields = ["guest_name", "text"]

    def clean_website(self):
        value = self.cleaned_data.get("website")
        if value:
            raise forms.ValidationError(_("Spam aniqlandi."))
        return value

    def clean_text(self):
        text = self.cleaned_data["text"].strip()
        if not text:
            raise forms.ValidationError(_("Izoh bo'sh bo'lishi mumkin emas."))
        return text


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="Ismingiz",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Ismingiz"}),
    )
    email = forms.EmailField(required=False, label="Email (ixtiyoriy)")

    class Meta:
        model = User
        fields = ["first_name", "username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Login (kirish uchun nom)"
        self.fields["username"].help_text = "Faqat tizimga kirish uchun ishlatiladi, boshqalarga ko'rinmaydi."
        self.fields["username"].error_messages = {
            "unique": "Bu login allaqachon band. Boshqa nom tanlang.",
            "required": "Login kiriting.",
            "invalid": "Loginda faqat harflar, raqamlar va @/./+/-/_ belgilaridan foydalaning.",
        }
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None


class SupportMessageForm(forms.ModelForm):

    class Meta:
        model = SupportMessage
        fields = ["message"]

        widgets = {
            "message": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": _("Savolingizni yozing...")
            })
        }