from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from apps.orders.models import Order
from .models import Payment
from .services import PaystackService


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

    if response["status"]:

        reference = response["data"]["reference"]

        Payment.objects.create(
            user=request.user,
            order=order,
            reference=reference,
            amount=order.total_price,
        )

        return redirect(
            response["data"]["authorization_url"]
        )

    return redirect("orders:checkout")

from django.http import HttpResponse


def payment_callback(request):

    reference = request.GET.get("reference")

    if not reference:
        return HttpResponse("Missing reference.", status=400)

    response = PaystackService.verify_payment(reference)

    if response["status"]:

        payment = Payment.objects.get(
            reference=reference
        )

        payment.status = "success"
        payment.transaction_id = str(
            response["data"]["id"]
        )
        payment.gateway_response = response
        payment.save()

        payment.order.status = "paid"
        payment.order.save()

        return redirect("accounts:downloads")

    return HttpResponse(
        "Payment verification failed.",
        status=400,
    )