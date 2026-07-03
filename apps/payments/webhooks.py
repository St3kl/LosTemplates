from apps.payments.models import Payment
from apps.downloads.services import DownloadService


def handle_success(payload):
    data = payload.get("data", {})
    reference = data.get("reference")

    if not reference:
        return {"status": "invalid_reference"}

    try:
        payment = Payment.objects.select_related("order").get(
            reference=reference
        )
    except Payment.DoesNotExist:
        return {"status": "not_found"}

    # idempotency check
    if payment.status == "success":
        return {"status": "already_processed"}

    # mark payment successful
    payment.status = "success"
    payment.transaction_id = str(data.get("id"))
    payment.gateway_response = payload
    payment.save()

    # update order
    order = payment.order

    if order.status != "paid":
        order.status = "paid"
        order.save()

    # 🔥 CRITICAL STEP — GRANT DOWNLOAD ACCESS
    # Give user access to ALL products in the order
    for item in order.items.select_related("product").all():
        DownloadService.grant_access(
            payment.user,
            item.product,
        )

    return {"status": "success"}