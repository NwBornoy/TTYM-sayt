import polib

for lang in ['en', 'ru', 'uz_Cyrl']:
    path = f'locale/{lang}/LC_MESSAGES/django.po'
    po = polib.pofile(path)
    seen = {}

    for entry in list(po):
        key = entry.msgid
        if key in seen:
            # Agar bu takroriy va tarjimasi bo'lsa, eski (bo'sh) yozuvga ko'chiramiz
            if entry.msgstr and not seen[key].msgstr:
                seen[key].msgstr = entry.msgstr
            po.remove(entry)
        else:
            seen[key] = entry

    po.save(path)
    print(f"{lang}: tozalandi, {len(po)} ta noyob msgid qoldi")