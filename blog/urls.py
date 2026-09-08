from django.urls import path, re_path
from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("biz-haqimizda/", views.AboutView.as_view(), name="about"),
    path("yangiliklar/", views.NewsListView.as_view(), name="news_list"),
    re_path(r"^yangiliklar/(?P<slug>[\w\-']+)/$", views.NewsDetailView.as_view(), name="news_detail"),
    path("galereya/", views.GalleryView.as_view(), name="gallery"),
    path("filiallar/", views.BranchesView.as_view(), name="branches"),
    path("maqolalar/", views.PostListView.as_view(), name="post_list"),
    re_path(r"^maqolalar/(?P<slug>[\w\-']+)/$", views.PostDetailView.as_view(), name="post_detail"),
    path("register/", views.register_view, name="register"),
    path("savol-javob/", views.support_chat, name="support_chat"),
    path('report-error/', views.report_error, name='report_error'),
    path('api/branches/', views.branches_api, name='branches_api'),
    path('report-error/', views.report_error, name='report_error'),
    path("rahbariyat/", views.LeadershipView.as_view(), name="leadership"),
    path("markaziy-apparat/", views.CentralStaffView.as_view(), name="central_staff"),
    path("korrupsiyaga-qarshi-kurashish/", views.AntiCorruptionListView.as_view(), name="anticorruption_list"),
    path("korrupsiyaga-qarshi-kurashish/<slug:slug>/", views.AntiCorruptionDetailView.as_view(), name="anticorruption_detail"),
    path("qonunlar/", views.LawListView.as_view(), name="law_list"),
    path("prezident-hujjatlari/", views.PresidentialDecreeListView.as_view(), name="decree_list"),
    path("hukumat-hujjatlari/", views.GovernmentDecreeListView.as_view(), name="gov_decree_list"),
    path("normativ-hujjatlar/", views.NormativeDocumentListView.as_view(), name="normative_list"),

    path("ekofaol/", views.EkoActivityListView.as_view(), name="eko_list"),
    re_path(r"^ekofaol/(?P<slug>[\w\-']+)/$", views.EkoActivityDetailView.as_view(), name="eko_detail"),
]