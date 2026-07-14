# import hmac
# import hashlib
# from django.conf import settings


# def verify_paystack_signature(request) -> bool:
#     """
#     Validates Paystack webhook signature using HMAC SHA-512.
#     """

#     signature = request.headers.get("x-paystack-signature")

#     if not signature:
#         return False

#     secret = settings.PAYSTACK_SECRET_KEY.encode("utf-8")
#     body = request.body

#     computed_signature = hmac.new(
#         secret,
#         body,
#         hashlib.sha512
#     ).hexdigest()

#     return hmac.compare_digest(computed_signature, signature)



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