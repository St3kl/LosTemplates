from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apps.orders.models import Order
from .models import Payment
from .services import PaystackService

from .utils import verify_paystack_signature
from .webhooks import process_webhook


def start_payment(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    callback_url = request.build_absolute_uri(
        reverse("payments:callback")
    )

    response = PaystackService.initialize_payment(
        request.user.email,
        order.total_price,
        callback_url,
    )

    if response.get("status"):

        reference = response["data"]["reference"]

        payment, created = Payment.objects.update_or_create(
            order=order,
            defaults={
                "user": request.user,
                "reference": reference,
                "amount": order.total_price,
                "status": "pending",
            },
        )

        return redirect(
            response["data"]["authorization_url"]
        )

    return HttpResponse(
        "Unable to initialize payment.",
        status=400,
    )


def payment_callback(request):

    reference = request.GET.get("reference")

    if not reference:
        return HttpResponse(
            "Missing payment reference.",
            status=400,
        )

    response = PaystackService.verify_payment(reference)

    if response.get("status"):

        payment = get_object_or_404(
            Payment,
            reference=reference,
        )

        payment.status = "success"
        payment.transaction_id = str(response["data"]["id"])
        payment.gateway_response = response
        payment.save()

        payment.order.status = "paid"
        payment.order.save()

        return redirect("accounts:downloads")

    return HttpResponse(
        "Payment verification failed.",
        status=400,
    )


import hashlib
import hmac
import json

from django.conf import settings
from django.http import HttpResponse


@csrf_exempt
def paystack_webhook(request):

    if request.method != "POST":
        return HttpResponse(status=405)

    # 1. Verify signature FIRST
    if not verify_paystack_signature(request):
        return HttpResponse(status=403)

    # 2. Parse payload
    payload = json.loads(request.body.decode("utf-8"))

    # 3. Process event
    process_webhook(payload)

    return HttpResponse(status=200)