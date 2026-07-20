import uuid
import requests

from django.conf import settings

from django.db import transaction

from apps.analytics.services import AnalyticsService
from apps.coupons.services import CouponService
from apps.downloads.services import DownloadService
from apps.notifications.services import NotificationService
from apps.payments.models import Payment


class PaystackService:

    BASE_URL = "https://api.paystack.co"

    @staticmethod
    def generate_reference():
        return str(uuid.uuid4())

    @staticmethod
    def initialize_payment(email, amount, callback_url):

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "email": email,
            "amount": int(amount * 100),  # Convert to smallest currency unit
            "reference": PaystackService.generate_reference(),
            "callback_url": callback_url,
        }

        response = requests.post(
            f"{PaystackService.BASE_URL}/transaction/initialize",
            json=payload,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def verify_payment(reference):

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }

        response = requests.get(
            f"{PaystackService.BASE_URL}/transaction/verify/{reference}",
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()
    
    @staticmethod
    @transaction.atomic
    def complete_payment(
        payment,
        gateway_response,
    ):
        """
        Complete a successful payment exactly once.
        """

        locked_payment = (
            Payment.objects
            .select_for_update()
            .select_related(
                "order",
                "user",
            )
            .get(
                id=payment.id,
            )
        )

        # Prevent duplicate processing.
        if locked_payment.status == "success":

            return {
                "status": "already_processed",
            }

        locked_payment.status = "success"

        locked_payment.transaction_id = str(
            gateway_response
            .get("data", {})
            .get("id"),
        )

        locked_payment.gateway_response = (
            gateway_response
        )

        locked_payment.save(
            update_fields=[
                "status",
                "transaction_id",
                "gateway_response",
                "updated_at",
            ],
        )

        order = locked_payment.order

        order.status = "paid"

        order.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        for item in order.items.select_related(
            "product",
        ):

            DownloadService.grant_access(
                locked_payment.user,
                item.product,
            )

            AnalyticsService.track_sale(
                product=item.product,
                user=locked_payment.user,
                price=item.price,
            )

            NotificationService.download_ready(
                locked_payment.user,
                item.product,
            )

        NotificationService.order_confirmation(
            locked_payment.user,
            order,
        )

        NotificationService.payment_success(
            locked_payment.user,
            locked_payment,
        )

        if order.coupon:

            CouponService.mark_used(
                order.coupon,
            )

        return {
            "status": "success",
        }