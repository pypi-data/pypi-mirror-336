from typing import override

from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel
from tinymce.models import HTMLField


class AbstractEmailConfiguration(SingletonModel):
    activated = models.BooleanField(
        default=False,
        verbose_name=_("Email está ativado?"),
        help_text=_(
            "Make sure to test the email in the button above before "
            "ticking this. When activated, notifications are going to "
            "be sent by email and it will be possible for users to "
            "redefine their.passwords"
        ),
    )
    host = models.CharField(
        max_length=128,
        verbose_name=_("Host"),
        default="smtp.gmail.com",
    )
    port = models.PositiveIntegerField(
        verbose_name=_("Port"),
        default=587,
    )
    username = models.CharField(
        max_length=128,
        verbose_name=_("User"),
        default="example@gmail.com",
    )
    password = models.CharField(
        max_length=128,
        verbose_name=_("Password"),
        default="1234",
    )
    use_tls = models.BooleanField(
        default=True,
        verbose_name=_("Use TLS"),
    )
    use_ssl = models.BooleanField(
        default=False,
        verbose_name=_("Use SSL"),
    )
    timeout = models.IntegerField(
        blank=True,
        null=True,
        default=120,
        verbose_name=_("Timeout"),
    )
    from_name = models.CharField(
        max_length=255,
        verbose_name=_("Sender name"),
        null=True,
        blank=True,
    )
    from_email = models.EmailField(
        verbose_name=_("Sender email"),
        default="admin@example.com",
    )
    signature = HTMLField(
        blank=True,
        null=True,
        verbose_name=_("Email signature"),
        help_text=format_html(
            "{} <code>{}</code>{}",
            _("To use this signature in email, use the variable"),
            "{{ signature }}",
            ".",
        ),
    )

    @override
    def __str__(self):
        return str(self._meta.verbose_name)

    class Meta:
        verbose_name = _("Email configuration")
        abstract = True


class EmailConfiguration(AbstractEmailConfiguration):
    pass
