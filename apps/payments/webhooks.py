import json

from apps.payments.models import Payment
from apps.notifications.services import NotificationService
from apps.downloads.services import DownloadService
from apps.coupons.services import CouponService


def process_webhook(payload):
    """
    Handles Paystack webhook events.
    """

    event = payload.get("event")

    if event == "charge.success":
        return handle_success(payload)

    return {"status": "ignored"}


def handle_success(payload):
    """
    Handle a successful Paystack payment.
    """

    data = payload.get("data", {})
    reference = data.get("reference")

    if not reference:
        return {"status": "invalid_reference"}

    # 🔐 STEP 1: Fetch payment once
    try:
        payment = Payment.objects.select_for_update().get(
            reference=reference
        )
    except Payment.DoesNotExist:
        return {"status": "not_found"}

    # 🚫 STEP 2: Prevent duplicate processing
    if payment.status == "success":
        return {"status": "already_processed"}

    # 💳 STEP 3: Mark payment as successful
    payment.status = "success"
    payment.transaction_id = str(data.get("id"))
    payment.gateway_response = payload
    payment.save()

    # 📦 STEP 4: Mark order as paid
    order = payment.order
    order.status = "paid"
    order.save()

    if order.status != "paid":
        order.status = "paid"
        order.save()

    # 🔔 STEP 5: Create notifications
    NotificationService.order_confirmation(
        payment.user,
        order,
    )

    NotificationService.payment_success(
        payment.user,
        payment,
    )
    # Coupon usage tracking
    if order.coupon:

        CouponService.mark_used(
        order.coupon
    )

    # 📥 STEP 6: Grant download access
    for item in order.items.all():

        DownloadService.grant_access(
            payment.user,
            item.product,
        )

        NotificationService.download_ready(
            payment.user,
            item.product,
        )
    

        

    return {"status": "success"}