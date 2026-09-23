from .models import Testimonial, Comment, ErrorReport, SupportMessage, NewUserNotification


def admin_notifications(request):
    if not request.path.startswith('/admin/'):
        return {}

    if not request.user.is_authenticated or not request.user.is_staff:
        return {}

    pending_testimonials = Testimonial.objects.filter(is_approved=False).order_by('-created_at')
    pending_comments = Comment.objects.filter(is_approved=False).order_by('-created_at')
    pending_errors = ErrorReport.objects.filter(is_resolved=False).order_by('-created_at')
    unread_messages = SupportMessage.objects.filter(is_admin=False, is_read=False).order_by('-created_at')
    new_users = NewUserNotification.objects.filter(is_seen=False).order_by('-created_at')

    notifications = []

    for t in pending_testimonials[:5]:
        notifications.append({
            'text': f"\U0001F4AC {t.name} fikr qoldirdi: \u201c{t.text[:35]}\u2026\u201d",
            'url': f"/admin/blog/testimonial/{t.id}/change/",
        })

    for c in pending_comments[:5]:
        notifications.append({
            'text': f"\U0001F4DD {c.display_name} izoh qoldirdi: \u201c{c.text[:35]}\u2026\u201d",
            'url': f"/admin/blog/comment/{c.id}/change/",
        })

    for e in pending_errors[:5]:
        notifications.append({
            'text': f"\u26A0\uFE0F Xato haqida xabar: \u201c{e.selected_text[:35]}\u2026\u201d",
            'url': f"/admin/blog/errorreport/{e.id}/change/",
        })

    for m in unread_messages[:5]:
        notifications.append({
            'text': f"\U0001F4E9 {m.sender.username} savol yubordi: \u201c{m.message[:35]}\u2026\u201d",
            'url': "/admin/blog/supportmessage/",
        })

    for n in new_users[:5]:
        notifications.append({
            'text': f"\U0001F195 Yangi foydalanuvchi ro'yxatdan o'tdi: {n.user.username}",
            'url': f"/admin/blog/newusernotification/{n.id}/change/",
        })

    total = (
        pending_testimonials.count()
        + pending_comments.count()
        + pending_errors.count()
        + unread_messages.count()
        + new_users.count()
    )

    return {
        'admin_notifications': notifications,
        'admin_notifications_count': total,
    }