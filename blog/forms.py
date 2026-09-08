from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SupportMessage
from .models import Comment


class CommentForm(forms.ModelForm):
    guest_name = forms.CharField(
        label="Ismingiz",
        max_length=80,
        required=False,
        help_text="Ixtiyoriy — bo'sh qoldirsangiz 'Anonim' deb ko'rsatiladi.",
        widget=forms.TextInput(attrs={"placeholder": "Ismingiz (ixtiyoriy)"}),
    )
    text = forms.CharField(
        label="Izoh",
        max_length=2000,
        widget=forms.Textarea(attrs={"placeholder": "Izohingizni yozing…", "rows": 4}),
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
            raise forms.ValidationError("Spam aniqlandi.")
        return value

    def clean_text(self):
        text = self.cleaned_data["text"].strip()
        if not text:
            raise forms.ValidationError("Izoh bo'sh bo'lishi mumkin emas.")
        return text


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label="Email (ixtiyoriy)")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class SupportMessageForm(forms.ModelForm):

    class Meta:
        model = SupportMessage
        fields = ["message"]

        widgets = {
            "message": forms.Textarea(attrs={
                "rows":2,
                "placeholder":"Savolingizni yozing..."
            })
        }
