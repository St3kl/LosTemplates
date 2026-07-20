import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from apps.orders.models import Order

from .models import Payment
from .services import PaystackService
from .utils import verify_paystack_signature
from .webhooks import process_webhook

# ==========================================================

# START PAYMENT

# ==========================================================

@login_required
def start_payment(request, order_id):
    """
    Initialize payment for a pending order.
    """


    order = get_object_or_404(
    Order,
    id=order_id,
    user=request.user,
)

# Prevent paying an already paid order.
    if order.status == "paid":

        return redirect(
        "accounts:downloads",
    )

# Calculate the final amount after discounts.
    final_amount = order.final_price

# Prevent unnecessary payment initialization.
    if final_amount <= 0:

        return redirect(
        "orders:order_success",
    )

    callback_url = request.build_absolute_uri(
        reverse(
            "payments:callback",
        )
    )

    response = PaystackService.initialize_payment(
        email=request.user.email,
        amount=final_amount,
        callback_url=callback_url,
    )

    if not response.get("status"):

        return HttpResponse(
            "Unable to initialize payment.",
            status=400,
        )

    reference = response["data"]["reference"]

    Payment.objects.update_or_create(
        order=order,
        defaults={
            "user": request.user,
            "reference": reference,
            "amount": final_amount,
            "status": "pending",
        },
    )

    return redirect(
        response["data"]["authorization_url"],
    )


# ==========================================================

# PAYMENT CALLBACK

# ==========================================================

@login_required
def payment_callback(request):
    """
    Verify a payment after Paystack redirects the user back.
    """


    reference = request.GET.get(
        "reference",
    )

    if not reference:

        return HttpResponse(
            "Missing payment reference.",
            status=400,
        )

    response = PaystackService.verify_payment(
        reference,
    )

    if not response.get("status"):

        return HttpResponse(
            "Payment verification failed.",
            status=400,
        )

    if response["data"]["status"] != "success":

        return HttpResponse(
            "Payment was not successful.",
            status=400,
        )

    payment = get_object_or_404(
        Payment,
        reference=reference,
    )

    # Verify the amount paid.
    expected_amount = int(
        payment.amount * 100,
    )

    if response["data"]["amount"] != expected_amount:

        return HttpResponse(
            "Payment amount mismatch.",
            status=400,
        )

# Verify the customer email.
    customer_email = (
        response["data"]
        .get("customer", {})
        .get("email")
    )

    if customer_email != payment.user.email:

        return HttpResponse(
            "Customer verification failed.",
            status=400,
        )

# Complete the payment through the centralized
# idempotent payment service.
    PaystackService.complete_payment(
        payment=payment,
        gateway_response=response,
    )

    return redirect(
        "accounts:downloads",
    )


# ==========================================================

# PAYSTACK WEBHOOK

# ==========================================================

@csrf_exempt
def paystack_webhook(request):
    """
    Process Paystack webhook events.
    """


    if request.method != "POST":

        return HttpResponse(
            status=405,
        )

# Verify Paystack webhook signature.
    if not verify_paystack_signature(
        request,
    ):

        return HttpResponse(
            status=403,
        )

    try:

        payload = json.loads(
            request.body.decode(
            "utf-8",
            )
        )

    except json.JSONDecodeError:

        return HttpResponse(
            status=400,
        )

    process_webhook(
        payload,
    )

    return HttpResponse(
        status=200,
    )

