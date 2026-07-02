from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [

    path(
        "pay/<int:order_id>/",
        views.start_payment,
        name="start",
    ),

    path(
        "callback/",
        views.payment_callback,
        name="callback",
    ),

    path(
        "webhook/",
        views.paystack_webhook,
        name="webhook",
    ),
]


import hashlib
import hmac
import json

from django.conf import settings


def verify_paystack_signature(request):
    """
    Verify the Paystack webhook signature.
    Returns True if the signature matches.
    """

    signature = request.headers.get("x-paystack-signature")

    if not signature:
        return False

    computed = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode(),
        request.body,
        hashlib.sha512,
    ).hexdigest()

    return hmac.compare_digest(signature, computed)