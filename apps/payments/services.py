import requests
from django.conf import settings


PAYSTACK_URL = "https://api.paystack.co/transaction/initialize"


def initialize_paystack_payment(email, amount, reference):

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "email": email,
        "amount": int(amount * 100),  # convert to kobo/pesewas
        "reference": reference,
    }

    response = requests.post(PAYSTACK_URL, json=data, headers=headers)

    return response.json()

import uuid
import requests

from django.conf import settings


class PaystackService:

    BASE_URL = "https://api.paystack.co"

    @staticmethod
    def generate_reference():
        return str(uuid.uuid4())

    @staticmethod
    def initialize_payment(email, amount, callback_url):

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        reference = PaystackService.generate_reference()

        payload = {
            "email": email,
            "amount": int(amount * 100),
            "reference": reference,
            "callback_url": callback_url,
        }

        response = requests.post(
            f"{PaystackService.BASE_URL}/transaction/initialize",
            json=payload,
            headers=headers,
            timeout=30,
        )

        return response.json()

    @staticmethod
    def verify_payment(reference):

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }

        response = requests.get(
            f"{PaystackService.BASE_URL}/transaction/verify/{reference}",
            headers=headers,
            timeout=30,
        )

        return response.json()