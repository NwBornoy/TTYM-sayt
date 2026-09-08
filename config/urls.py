from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.conf.urls.static import static


urlpatterns = [
    # Admin panel
    path(settings.ADMIN_URL, admin.site.urls),

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

    # CKEditor 5 (rasm yuklash va boshqa xizmatlar uchun)
    path("ckeditor5/", include("django_ckeditor_5.urls")),

    # Blog ilovasi
    path(
        "",
        include("blog.urls")
    ),
]


# Media rasmlarni DEBUG rejimida ko'rsatish
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )