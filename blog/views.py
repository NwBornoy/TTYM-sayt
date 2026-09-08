from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .models import SupportMessage, SupportTicket, News, Gallery, Branch, ContactInfo,Partner,UsefulLink,EkoActivity
from .forms import SupportMessageForm
from .forms import CommentForm, RegisterForm
from .models import Post
from django.db.models import Q
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .models import ErrorReport
from django.http import JsonResponse
from .models import Branch  # agar allaqachon import qilinmagan bo'lsa
from .models import Leader
from .models import StaffMember
from .models import AntiCorruptionPost
from .models import Law
from .models import PresidentialDecree
from .models import GovernmentDecree
from .models import NormativeDocument


class NormativeDocumentListView(ListView):
    """Markaz normativ hujjatlari."""
    model = NormativeDocument
    template_name = "blog/normative_list.html"
    context_object_name = "documents"

    def get_queryset(self):
        return NormativeDocument.objects.filter(is_published=True).order_by("order", "-created_at")


class GovernmentDecreeListView(ListView):
    """Hukumat qarori va farmoyishlari."""
    model = GovernmentDecree
    template_name = "blog/gov_decree_list.html"
    context_object_name = "decrees"

    def get_queryset(self):
        return GovernmentDecree.objects.filter(is_published=True).order_by("order", "-created_at")


class PresidentialDecreeListView(ListView):
    """Prezident farmon, qaror va farmoyishlari."""
    model = PresidentialDecree
    template_name = "blog/decree_list.html"
    context_object_name = "decrees"

    def get_queryset(self):
        return PresidentialDecree.objects.filter(is_published=True).order_by("order", "-created_at")


class LawListView(ListView):
    """Qonunlar ro'yxati."""
    model = Law
    template_name = "blog/law_list.html"
    context_object_name = "laws"

    def get_queryset(self):
        return Law.objects.filter(is_published=True).order_by("order", "-created_at")


class AntiCorruptionListView(ListView):
    """Korrupsiyaga qarshi kurashish - mavzular ro'yxati."""
    model = AntiCorruptionPost
    template_name = "blog/anticorruption_list.html"
    context_object_name = "topics"

    def get_queryset(self):
        return AntiCorruptionPost.objects.filter(is_published=True).order_by("order", "-created_at")


class AntiCorruptionDetailView(DetailView):
    """Korrupsiyaga qarshi kurashish - mavzu tafsilotlari."""
    model = AntiCorruptionPost
    template_name = "blog/anticorruption_detail.html"
    context_object_name = "topic"
    slug_field = "slug"

    def get_queryset(self):
        return AntiCorruptionPost.objects.filter(is_published=True)

class CentralStaffView(ListView):
    """Markaziy apparat."""
    model = StaffMember
    template_name = "blog/central_staff.html"
    context_object_name = "staff_members"

    def get_queryset(self):
        return StaffMember.objects.all().order_by("order", "id")


class LeadershipView(ListView):
    """Rahbariyat."""
    model = Leader
    template_name = "blog/leadership.html"
    context_object_name = "leaders"

    def get_queryset(self):
        return Leader.objects.all().order_by("order", "id")


class EkoActivityListView(ListView):
    """Ekofaol xodim - obodonlashtirish postlari ro'yxati."""
    model = EkoActivity
    template_name = "blog/eko_list.html"
    context_object_name = "activities"
    paginate_by = 9

    def get_queryset(self):
        return EkoActivity.objects.filter(is_published=True).order_by("-created_at")


class EkoActivityDetailView(DetailView):
    """Ekofaol xodim posti tafsilotlari."""
    model = EkoActivity
    template_name = "blog/eko_detail.html"
    context_object_name = "activity"
    slug_field = "slug"

    def get_queryset(self):
        return EkoActivity.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comments"] = self.object.approved_comments
        ctx["comment_form"] = CommentForm()
        return ctx

    def post(self, request, *args, **kwargs):
        """Izoh yuborishni qayta ishlaydi."""
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.activity = self.object
            if request.user.is_authenticated:
                comment.user = request.user
                comment.guest_name = ""
            comment.is_approved = False
            comment.save()
            messages.success(
                request,
                "Izohingiz qabul qilindi. U moderatsiyadan o'tgach saytda ko'rinadi.",
            )
            return redirect(self.object.get_absolute_url())

        ctx = self.get_context_data()
        ctx["comment_form"] = form
        return self.render_to_response(ctx)
def branches_api(request):
    branches = Branch.objects.exclude(slug="")
    data = {}

    for b in branches:
        data[b.slug] = {
            "name": b.name,
            "director": f"Rahbar: {b.director_name}" if b.director_name else "Rahbar: __________",
            "phone": f"Telefon: {b.phone}" if b.phone else "Telefon: __________",
            "address": b.address,
            "email": b.email,
            "telegram": b.telegram or "#",
            "instagram": b.instagram or "#",
            "image": b.director_image.url if b.director_image else "",
            "is_main": b.is_main,
        }

    return JsonResponse(data)

@require_POST
@csrf_protect
def report_error(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "invalid_data"}, status=400)

    selected_text = (data.get("selected_text") or "").strip()
    page_url = (data.get("page_url") or "")[:500]

    if not selected_text:
        return JsonResponse({"ok": False, "error": "empty_text"}, status=400)

    ErrorReport.objects.create(
        page_url=page_url,
        selected_text=selected_text[:5000],
        user=request.user if request.user.is_authenticated else None,
        ip_address=request.META.get("REMOTE_ADDR"),
    )

    return JsonResponse({"ok": True})


class HomeView(TemplateView):
    template_name = "blog/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["posts"] = Post.objects.filter(is_published=True).order_by("-created_at")[:3]

        news_list = list(News.objects.filter(is_published=True).order_by("-created_at")[:6])
        ctx["main_news"] = news_list[0] if news_list else None
        ctx["side_news"] = news_list[1:]

        ctx["contact"] = ContactInfo.objects.first()

        ctx["gallery_items"] = Gallery.objects.all().order_by("order")[:8]   # ← YANGI QATOR
        ctx["partners"] = Partner.objects.all()
        ctx["useful_links"] = UsefulLink.objects.all()

        return ctx


# views.py faylida AboutView klassini shu bilan ALMASHTIRING
# (import qatorida ContactInfo allaqachon bor, qo'shimcha import shart emas)

class AboutView(TemplateView):
    """Markaz haqida - filiallar bilan."""
    template_name = "blog/about.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["branches"] = Branch.objects.all().order_by("-is_main", "order")
        ctx["main_branch"] = Branch.objects.filter(is_main=True).first()

        # YANGI: galereyadan haqiqiy rasmlar
        ctx["about_gallery"] = Gallery.objects.filter(media_type="photo").order_by("order")[:6]

        # YANGI: call-markaz bo'limi uchun aloqa ma'lumotlari
        ctx["contact"] = ContactInfo.objects.first()

        return ctx


class NewsListView(ListView):
    """Markaz yangiliklari."""
    model = News
    template_name = "blog/news_list.html"
    context_object_name = "news"
    paginate_by = 6

    def get_queryset(self):
        queryset = News.objects.filter(is_published=True).order_by("-created_at")
        search = self.request.GET.get("q", "").strip()
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        return queryset


class NewsDetailView(DetailView):
    """Yangilik tafsilotlari."""
    model = News
    template_name = "blog/news_detail.html"
    context_object_name = "news"
    slug_field = "slug"

    def get_queryset(self):
        return News.objects.filter(is_published=True)


class GalleryView(TemplateView):
    """Foto va videogalereya."""
    template_name = "blog/gallery.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["photos"] = Gallery.objects.filter(media_type="photo").order_by("order")
        ctx["videos"] = Gallery.objects.filter(media_type="video").order_by("order")
        return ctx


class BranchesView(TemplateView):
    """Barcha filiallar."""
    template_name = "blog/branches.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["branches"] = Branch.objects.all().order_by("-is_main", "order")
        return ctx


class PostListView(ListView):
    """Barcha maqolalar va qidiruv natijalari."""
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):

        queryset = Post.objects.filter(
            is_published=True
        ).order_by("-created_at")

        search = self.request.GET.get("q", "").strip()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )

        return queryset



class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        qs = Post.objects.all()
        if not self.request.user.is_staff:
            qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comments"] = self.object.approved_comments
        ctx["comment_form"] = CommentForm()
        return ctx

    def post(self, request, *args, **kwargs):
        """Izoh yuborishni qayta ishlaydi."""
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            if request.user.is_authenticated:
                comment.user = request.user
                comment.guest_name = ""
            comment.is_approved = False
            comment.save()
            messages.success(
                request,
                "Izohingiz qabul qilindi. U moderatsiyadan o'tgach saytda ko'rinadi.",
            )
            return redirect(self.object.get_absolute_url())

        ctx = self.get_context_data()
        ctx["comment_form"] = form
        return self.render_to_response(ctx)


def register_view(request):
    """Ro'yxatdan o'tish."""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz.")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def support_chat(request):

    ticket = SupportTicket.objects.filter(
        user=request.user
    ).exclude(
        status="closed"
    ).order_by("-updated_at").first()

    if request.method == "POST":

        form = SupportMessageForm(request.POST)

        if form.is_valid():

            if ticket is None:
                ticket = SupportTicket.objects.create(
                    user=request.user,
                    subject="Savol",
                    status="new",
                )

            msg = form.save(commit=False)

            msg.sender = request.user

            msg.is_admin = False

            msg.ticket = ticket

            msg.save()

            ticket.save()

            messages.success(
                request,
                "Savolingiz yuborildi."
            )

            return redirect("support_chat")

    else:
        form = SupportMessageForm()

    if request.user.is_staff:

        chats = SupportMessage.objects.select_related(
            "sender",
            "ticket",
        ).all()

    else:

        chats = SupportMessage.objects.filter(
            ticket__user=request.user
        ).select_related(
            "sender",
            "ticket",
        )

    chats = chats.order_by("created_at")

    return render(
        request,
        "blog/support_chat.html",
        {
            "messages_list": chats,
            "form": form,
        }
    )