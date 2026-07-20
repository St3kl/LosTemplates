from django.utils import timezone

from .email_service import EmailService
from .models import Notification


class NotificationService:
    """
    Central notification service.

    Every notification in LosTemplates should pass
    through this class.
    """

    @staticmethod
    def create(
        user,
        notification_type,
        title,
        message,
    ):
        return Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
        )

    @staticmethod
    def welcome(user):
        notification = NotificationService.create(
            user=user,
            notification_type="welcome",
            title="Welcome to LosTemplates!",
            message=(
                "Your account has been created successfully."
            ),
        )

        if user.email:

            EmailService.send_email(
                subject="Welcome to LosTemplates",
                recipient=user.email,
                template="emails/welcome.html",
                context={
                    "user": user,
                    "dashboard_url": (
                        "http://127.0.0.1:8000/"
                        "accounts/dashboard/"
                    ),
                    "year": timezone.now().year,
                },
            )

        return notification

    @staticmethod
    def order_confirmation(user, order):
        notification = NotificationService.create(
            user=user,
            notification_type="order",
            title="Order Confirmed",
            message=(
                f"Order #{order.id} has been confirmed."
            ),
        )

        if user.email:

            EmailService.send_email(
                subject="Order Confirmation",
                recipient=user.email,
                template="emails/order_confirmation.html",
                context={
                    "user": user,
                    "order": order,
                    "year": timezone.now().year,
                },
            )

        return notification

    @staticmethod
    def payment_success(user, payment):
        notification = NotificationService.create(
            user=user,
            notification_type="payment",
            title="Payment Successful",
            message=(
                "Your payment has been verified."
            ),
        )

        if user.email:

            EmailService.send_email(
                subject="Payment Successful",
                recipient=user.email,
                template="emails/payment_success.html",
                context={
                    "user": user,
                    "payment": payment,
                    "year": timezone.now().year,
                },
            )

        return notification

    @staticmethod
    def download_ready(user, product):
        notification = NotificationService.create(
            user=user,
            notification_type="download",
            title="Download Ready",
            message=(
                f"{product.title} is now available."
            ),
        )

        if user.email:

            EmailService.send_email(
                subject="Your Download is Ready",
                recipient=user.email,
                template="emails/download_ready.html",
                context={
                    "user": user,
                    "product": product,
                    "year": timezone.now().year,
                },
            )

        return notification

    @staticmethod
    def system(user, message):
        return NotificationService.create(
            user=user,
            notification_type="system",
            title="System Notification",
            message=message,
        )