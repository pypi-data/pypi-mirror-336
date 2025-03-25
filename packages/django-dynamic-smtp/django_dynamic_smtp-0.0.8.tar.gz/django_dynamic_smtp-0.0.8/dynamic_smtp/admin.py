from smtplib import SMTPException

from django.conf import settings
from django.contrib import admin, messages
from django.core import mail
from django.core.mail.backends.console import EmailBackend as ConsoleEmailBackend
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django_object_actions import DjangoObjectActions, action
from solo.admin import SingletonModelAdmin

from .models import AbstractEmailConfiguration, EmailConfiguration


class EmailConfigurationAdmin(DjangoObjectActions, SingletonModelAdmin):
    change_actions = ["test_email"]

    @action(
        label=_("Test email"),
        description=_(
            "Send a test email from the account configured below to the "
            "email registered as sender. Save before using."
        ),
    )
    def test_email(self, request: HttpRequest, obj: AbstractEmailConfiguration):
        host = request.get_host()
        try:
            with mail.get_connection() as connection:
                if type(connection) is ConsoleEmailBackend:
                    raise AssertionError(
                        _("Using debug backend. Try using DEBUG=False in settings")
                    )
                __ = mail.send_mail(
                    message=_(
                        "This email has been sent to verify if the "
                        "mailing system is well configured in the "
                        "administration of %(host)s. It seems so!"
                    )
                    % {"host": host},
                    from_email=obj.from_email,
                    subject=_("[%(host)s] Email test") % {"host": host},
                    recipient_list=[obj.from_email],
                    fail_silently=False,
                    connection=connection,
                )
        except (SMTPException, AssertionError) as e:
            messages.error(
                request,
                _("Email not well configured: %s") % str(e),
            )
            return

        messages.success(
            request,
            _("Email is well configured! :)"),
        )


if getattr(settings, "DYNAMIC_SMPT_REGISTER_ADMIN", True):
    admin.site.register(EmailConfiguration, EmailConfigurationAdmin)
