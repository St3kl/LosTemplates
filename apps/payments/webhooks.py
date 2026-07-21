# from django.db import transaction
# from django.utils import timezone

# from apps.analytics.services import AnalyticsService
# from apps.coupons.services import CouponService
# from apps.downloads.services import DownloadService
# from apps.notifications.services import NotificationService

# from .models import Payment
# from apps.payments.services import PaystackService


# def process_webhook(payload):
#     """
#     Route Paystack webhook events
#     to the appropriate handler.
#     """

#     event = payload.get("event")

#     if event == "charge.success":
#         return handle_success(payload)

#     return {
#         "status": "ignored",
#         "event": event,
#     }


# def handle_success(payload):

#     data = payload.get(
#         "data",
#         {},
#     )

#     reference = data.get(
#         "reference",
#     )

#     if not reference:

#         return {
#             "status": "invalid_reference",
#         }

#     try:

#         payment = Payment.objects.get(
#             reference=reference,
#         )

#     except Payment.DoesNotExist:

#         return {
#             "status": "not_found",
#         }

#         return PaystackService.complete_payment(
#             payment=payment,
#             gateway_response=payload,
#         )

#         # ---------------------------------
#         # PREVENT DUPLICATE PROCESSING
#         # ---------------------------------

#         if payment.status == "success":
#             return {
#                 "status": "already_processed",
#             }

#         # ---------------------------------
#         # MARK PAYMENT AS SUCCESSFUL
#         # ---------------------------------

#         payment.status = "success"

#         payment.transaction_id = str(
#             data.get("id")
#         )

#         payment.paid_at = timezone.now()

#         payment.gateway_response = payload

#         payment.save(
#             update_fields=[
#                 "status",
#                 "transaction_id",
#                 "paid_at",
#                 "gateway_response",
#                 "updated_at",
#             ]
#         )

#         # ---------------------------------
#         # MARK ORDER AS PAID
#         # ---------------------------------

#         order = payment.order

#         order.status = "paid"

#         order.save(
#             update_fields=[
#                 "status",
#                 "updated_at",
#             ]
#         )

#         # ---------------------------------
#         # PROCESS ORDER ITEMS
#         # ---------------------------------

#         order_items = (
#             order.items
#             .select_related(
#                 "product",
#             )
#             .all()
#         )

#         for item in order_items:

#             # -----------------------------
#             # ANALYTICS
#             # -----------------------------

#             AnalyticsService.track_sale(
#                 product=item.product,
#                 user=payment.user,
#                 price=item.price,
#             )

#             # -----------------------------
#             # GRANT DOWNLOAD ACCESS
#             # -----------------------------

#             DownloadService.grant_access(
#                 payment.user,
#                 item.product,
#             )

#         # ---------------------------------
#         # COUPON USAGE
#         # ---------------------------------

#         if order.coupon:

#             CouponService.mark_used(
#                 order.coupon,
#             )

#         # ---------------------------------
#         # ORDER NOTIFICATION
#         # ---------------------------------

#         NotificationService.order_confirmation(
#             payment.user,
#             order,
#         )

#         # ---------------------------------
#         # PAYMENT NOTIFICATION
#         # ---------------------------------

#         NotificationService.payment_success(
#             payment.user,
#             payment,
#         )

#         # ---------------------------------
#         # DOWNLOAD NOTIFICATIONS
#         # ---------------------------------

#         for item in order_items:

#             NotificationService.download_ready(
#                 payment.user,
#                 item.product,
#             )

#     return {
#         "status": "success",
#     }


from apps.payments.services import PaystackService
from .models import Payment


def process_webhook(payload):
    """
    Route Paystack webhook events
    to the appropriate handler.
    """

    event = payload.get("event")

    if event == "charge.success":

        return handle_success(
            payload,
        )

    return {
        "status": "ignored",
        "event": event,
    }


def handle_success(payload):
    """
    Process a successful Paystack charge.
    """

    data = payload.get(
        "data",
        {},
    )

    reference = data.get(
        "reference",
    )

    if not reference:

        return {
            "status": "invalid_reference",
        }

    try:

        payment = Payment.objects.get(
            reference=reference,
        )

    except Payment.DoesNotExist:

        return {
            "status": "not_found",
        }

    return PaystackService.complete_payment(
        payment=payment,
        gateway_response=payload,
    )
