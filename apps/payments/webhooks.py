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

    if not reference:
        return {"status": "invalid_reference"}

    # 🔐 STEP 1: Fetch payment once
    try:
        payment = Payment.objects.select_for_update().get(reference=reference)
    except Payment.DoesNotExist:
        return {"status": "not_found"}

    # 🚫 STEP 2: IDEMPOTENCY CHECK (CRITICAL)
    if payment.status == "success":
        return {"status": "already_processed"}

    # 💳 STEP 3: Mark payment success
    payment.status = "success"
    payment.transaction_id = str(data.get("id"))
    payment.gateway_response = payload
    payment.save()

    # 📦 STEP 4: Update order safely
    order = payment.order

    if order.status != "paid":
        order.status = "paid"
        order.save()

    return {"status": "success"}