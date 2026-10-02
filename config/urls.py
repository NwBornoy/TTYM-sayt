from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns



urlpatterns = [
    # Admin panel — tilga bog'liq emas, prefiks olmaydi
    path(settings.ADMIN_URL, admin.site.urls),

    # CKEditor 5 (rasm yuklash va boshqa xizmatlar uchun) — tilga bog'liq emas
    path("ckeditor5/", include("django_ckeditor_5.urls")),

    # Tilni almashtirish uchun maxsus yo'l (dropdown/forma shu yerga POST yuboradi)
    path("i18n/", include("django.conf.urls.i18n")),

    path("", include("telegram_bot.urls")),
]


# Tilga bog'liq sahifalar — bularga avtomatik /uz/, /ru/, /en/, /uz-cyrl/ prefiksi qo'shiladi
urlpatterns += i18n_patterns(
    # Login
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),

    # Logout
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    # Blog ilovasi
    path(
        "",
        include("blog.urls")
    ),

    prefix_default_language=True,  # /uz/ ham ko'rinsin (False qilsangiz asosiy til prefikssiz qoladi)
)


# Media rasmlarni DEBUG rejimida ko'rsatish
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )