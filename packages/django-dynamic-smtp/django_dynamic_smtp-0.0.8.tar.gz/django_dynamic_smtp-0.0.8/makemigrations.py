from pathlib import Path

from django import setup
from django.conf import settings
from django.core.management import call_command

BASE_DIR = Path(__file__).resolve().parent


def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        },
        INSTALLED_APPS=(
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "dynamic_smtp",
        ),
    )

    setup()


boot_django()
__ = call_command("makemigrations", "dynamic_smtp")
