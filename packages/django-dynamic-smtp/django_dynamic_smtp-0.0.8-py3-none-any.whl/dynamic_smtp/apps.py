from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DynamicSmtpConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dynamic_smtp"
    verbose_name = _("Email configuration")
