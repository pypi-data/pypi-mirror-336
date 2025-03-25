from collections.abc import Sequence

from bs4 import BeautifulSoup
from django.apps import apps
from django.conf import settings
from django.core import mail
from django.core.exceptions import ImproperlyConfigured
from django.core.mail.backends.smtp import EmailBackend

from .models import EmailConfiguration as DefaultEmailConfiguration

EmailConfiguration = DefaultEmailConfiguration

conf_model = getattr(settings, "DYNAMIC_SMPT_EMAIL_CONFIGURATION_MODEL", None)
if conf_model:
    try:
        EmailConfiguration = apps.get_model(conf_model)
    except ValueError as error:
        raise ImproperlyConfigured(error) from error


class DynamicSMPTEmailBackend(EmailBackend):
    def __init__(
        self,
        host: str | None = None,
        port: str | None = None,
        username: str | None = None,
        password: str | None = None,
        use_tls: str | None = None,
        fail_silently: bool = False,
        use_ssl: str | None = None,
        timeout: str | None = None,
        ssl_keyfile: str | None = None,
        ssl_certfile: str | None = None,
        **kwargs: ...,
    ):
        conf = EmailConfiguration.get_solo()

        super().__init__(
            host=host or conf.host,
            port=port or conf.port,
            username=username or conf.username,
            password=password or conf.password,
            use_tls=use_tls or conf.use_tls,
            fail_silently=fail_silently,
            use_ssl=use_ssl or conf.use_ssl,
            timeout=timeout or conf.timeout,
            ssl_keyfile=ssl_keyfile,
            ssl_certfile=ssl_certfile,
            **kwargs,
        )


def html2text(html: str):
    return BeautifulSoup(html, "lxml").get_text()


def send_mail(
    subject: str,
    message: str,
    recipients: Sequence[str] | str,
):
    mailconf = EmailConfiguration.get_solo()
    recipient_list = (
        recipients.split(",") if isinstance(recipients, str) else recipients
    )

    return mail.send_mail(
        subject,
        html2text(message),
        recipient_list=recipient_list,
        html_message=message,
        fail_silently=False,
        auth_user=mailconf.username,
        auth_password=mailconf.password,
        from_email=mailconf.from_email,
    )
