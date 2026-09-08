# Qashqadaryo TTY — Maqolalar va izohlar (Django)

## Nima qilingan

- **Post** modeli — adminlar/xodimlar Django'ning o'zining tayyor admin panelida
  (`/admin/`) maqola yozadi, tahrirlaydi, o'chiradi. Bu panel Django tomonidan
  yillar davomida sinovdan o'tgan, xavfsiz autentifikatsiya va ruxsatlar tizimiga ega.
- **Comment** modeli — har qanday tashrifchi (ro'yxatdan o'tgan yoki mehmon) izoh qoldira oladi.
  Yangi izohlar standart holatda **tasdiqlanmagan** holatda saqlanadi va admin panelda
  tasdiqlangandan keyingina saytda ko'rinadi (spam va haqoratdan himoya).
- Ro'yxatdan o'tish ixtiyoriy — foydalanuvchi xohlasa hisob ochib, o'z ismi bilan
  izoh qoldirishi mumkin, yoki hech qanday hisobsiz "mehmon" sifatida yozishi mumkin.

## Xavfsizlik bo'yicha nima ta'minlangan

| Xavf | Qanday yopilgan |
|---|---|
| Parollar ochiq saqlanishi | Django parollarni avtomatik xesh (PBKDF2/Argon2) qilib saqlaydi |
| CSRF hujumi | Har bir formada `{% csrf_token %}`, `CsrfViewMiddleware` yoqilgan |
| XSS (zararli skript kiritish) | Django shablonlari matnni avtomatik escape qiladi (`{{ comment.text }}`) |
| SQL in'eksiya | Django ORM ishlatilgan, xom SQL yo'q |
| Spam-botlar | Honeypot maydon (`website`) + izohlar moderatsiyasi |
| Admin manzilini topish | `/admin/` o'rniga `.env` orqali maxsus manzil qo'yish mumkin |
| Kuchsiz parollar | `AUTH_PASSWORD_VALIDATORS` — kamida 10 belgi, oddiy parollar taqiqlangan |
| HTTP orqali tinglash | Production'da (`DEBUG=False`) HTTPS majburiy, cookie'lar faqat HTTPS orqali |
| Maxfiy kalitlar kodga yozilishi | `SECRET_KEY`, `ALLOWED_HOSTS` va h.k. `.env` fayldan o'qiladi, git'ga qo'shilmaydi |

**Qo'shimcha tavsiya etiladigan qadamlar (ushbu loyihaga kiritilmagan, lekin production uchun muhim):**
- `django-axes` yoki shunga o'xshash paket bilan login formasiga brute-force himoyasi qo'yish
- Izoh formasiga captcha (masalan `django-recaptcha`) qo'shish, agar spam ko'p bo'lsa
- Muntazam zaxira nusxa (backup) va `pip-audit` / `safety` bilan kutubxonalarni tekshirish
- Serverni Nginx + Gunicorn + HTTPS sertifikat (Let's Encrypt) bilan sozlash

## O'rnatish (lokal sinov uchun)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # so'ng .env faylini o'zingiznikiga moslang

python manage.py migrate
python manage.py createsuperuser   # admin hisobini yaratish
python manage.py runserver
```

Brauzerda oching:
- Sayt: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Production'ga chiqarish (qisqacha)

1. `.env` faylida `DJANGO_DEBUG=False`, haqiqiy `DJANGO_SECRET_KEY`,
   `DJANGO_ALLOWED_HOSTS=sizningdomeningiz.uz` qo'ying.
2. PostgreSQL ishlatish tavsiya etiladi — `DATABASE_URL` orqali ulang.
3. `python manage.py collectstatic` — statik fayllarni yig'ish.
4. Gunicorn + Nginx orqali ishga tushiring, HTTPS sertifikat o'rnating.
5. `python manage.py createsuperuser` — birinchi admin hisobini yarating.

## Qanday ishlatiladi

- **Admin (siz yoki xodim):** `/admin/` manziliga kirib, "Maqolalar" bo'limidan
  "Qo'shish" tugmasi orqali yangi maqola yozasiz. Muallif avtomatik sizning
  hisobingiz bo'lib belgilanadi.
- **Izohlarni moderatsiya qilish:** `/admin/` → "Izohlar" bo'limida yangi izohlarni
  ko'rasiz, "Tasdiqlangan" ustunini belgilab yoki ro'yxatdan checkbox tanlab
  "Tanlangan izohlarni tasdiqlash" amalini bajarasiz — shundan keyin izoh saytda chiqadi.
- **Tashrifchilar:** Bosh sahifada maqolalarni o'qiydi, har bir maqola ostida
  ism kiritib (yoki kiritmasdan) izoh qoldiradi.
