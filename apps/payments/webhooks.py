import json


def process_webhook(payload):
    """
    Handles Paystack webhook events.
    """

    event = payload.get("event")

    if event == "charge.success":
        return handle_success(payload)

    return {"status": "ignored"}


from apps.payments.models import Payment
from apps.orders.models import Order


def handle_success(payload):
    data = payload.get("data", {})
    reference = data.get("reference")

    try:
        payment = Payment.objects.get(reference=reference)
    except Payment.DoesNotExist:
        return {"status": "not_found"}

    # Prevent duplicate processing
    if payment.status == "success":
        return {"status": "already_processed"}

    payment.status = "success"
    payment.transaction_id = str(data.get("id"))
    payment.gateway_response = payload
    payment.save()

    order = payment.order
    order.status = "paid"
    order.save()

    return {"status": "success"}