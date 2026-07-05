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

        return NotificationService.create(
            user=user,
            notification_type="welcome",
            title="Welcome to LosTemplates",
            message=(
                "Your account has been created successfully."
            ),
        )

    @staticmethod
    def order_confirmation(user, order):

        return NotificationService.create(
            user=user,
            notification_type="order",
            title="Order Confirmed",
            message=(
                f"Your order #{order.id} has been received."
            ),
        )

    @staticmethod
    def payment_success(user, payment):

        return NotificationService.create(
            user=user,
            notification_type="payment",
            title="Payment Successful",
            message=(
                f"Payment reference "
                f"{payment.reference} "
                f"was completed successfully."
            ),
        )

    @staticmethod
    def download_ready(user, product):

        return NotificationService.create(
            user=user,
            notification_type="download",
            title="Download Ready",
            message=(
                f"{product.title} is now available "
                f"in your Downloads."
            ),
        )

    @staticmethod
    def system(user, message):

        return NotificationService.create(
            user=user,
            notification_type="system",
            title="System Notification",
            message=message,
        )