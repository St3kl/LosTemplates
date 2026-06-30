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