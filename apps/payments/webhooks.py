import json


def process_webhook(payload):
    """
    Placeholder for Paystack webhook processing.
    We'll implement event handling next.
    """

    event = payload.get("event")

    return event