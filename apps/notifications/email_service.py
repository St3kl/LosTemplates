from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailService:
    """
    Centralized email service.
    """

    @staticmethod
    def send_email(
        subject,
        recipient,
        template,
        context=None,
    ):
        """
        Send an HTML email with a plain-text fallback.
        """

        if context is None:
            context = {}

        html_message = render_to_string(
            template,
            context,
        )

        plain_message = strip_tags(
            html_message,
        )

        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
        )

        email.attach_alternative(
            html_message,
            "text/html",
        )

        email.send()