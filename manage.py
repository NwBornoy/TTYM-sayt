#!/usr/bin/env python
"""Django administrativ vazifalar uchun buyruq qatori vositasi."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django o'rnatilmagan yoki virtual muhit faollashtirilmagan. "
            "requirements.txt faylidagi paketlarni o'rnating: pip install -r requirements.txt"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
