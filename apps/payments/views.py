import uuid
import requests

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apps.orders.models import Order


PAYSTACK_URL = "https://api.paystack.co/transaction/initialize"


def initialize_paystack_payment(email, amount, reference):
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "email": email,
        "amount": int(amount * 100),   # smallest currency unit
        "reference": reference,
        "callback_url": settings.PAYSTACK_CALLBACK_URL,
    }

    response = requests.post(
        PAYSTACK_URL,
        json=data,
        headers=headers,
    )

    return response.json()


def start_payment(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    reference = str(uuid.uuid4())

    response = initialize_paystack_payment(
        request.user.email,
        order.total_price,
        reference,
    )

    if response.get("status"):

        return redirect(
            response["data"]["authorization_url"]
        )

    return HttpResponse(
        "Unable to initialize payment.",
        status=400,
    )


@csrf_exempt
def paystack_webhook(request):
    return HttpResponse(status=200)