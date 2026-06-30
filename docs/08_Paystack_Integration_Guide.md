# 08_Paystack_Integration_Guide.md

# LosTemplates Paystack Integration Guide

**Project:** LosTemplates
**Version:** 0.3.0
**Payment Provider:** Paystack
**Region:** Ghana-friendly (supports GHS, USD, NGN)

---

# 1. Purpose

This document defines how payments are handled in LosTemplates using Paystack.

It ensures:

* Secure payment processing
* Reliable order verification
* Fraud prevention
* Automated order fulfillment
* Clean transaction tracking

---

# 2. Why Paystack

Paystack is used because:

* Fully supported in Ghana
* Easy Django integration
* Strong API + webhooks
* Supports cards, mobile money, bank transfers
* Reliable transaction verification system

---

# 3. Payment Flow Architecture

```text id="flow1"
User clicks "Buy"
        ↓
Create Pending Order
        ↓
Redirect to Paystack Checkout
        ↓
User Pays
        ↓
Paystack Sends Webhook
        ↓
Verify Transaction
        ↓
Mark Order as Paid
        ↓
Unlock Downloads
```

---

# 4. Required Settings

Add to `settings.py`:

```python id="cfg1"
PAYSTACK_SECRET_KEY = "your_secret_key"
PAYSTACK_PUBLIC_KEY = "your_public_key"
PAYSTACK_CALLBACK_URL = "http://127.0.0.1:8000/payments/verify/"
```

Use environment variables in production.

---

# 5. Install Requirements

```bash id="inst1"
pip install requests
```

---

# 6. Payment Initialization

Create `payments/services.py`

```python id="svc1"
import requests
from django.conf import settings


def initialize_payment(email, amount, reference):
    url = "https://api.paystack.co/transaction/initialize"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "email": email,
        "amount": int(amount * 100),  # convert to kobo/pesewas
        "reference": reference,
        "callback_url": settings.PAYSTACK_CALLBACK_URL,
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()
```

---

# 7. Payment View

```python id="view1"
@login_required
def pay_for_order(request, order_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)

    response = initialize_payment(
        email=request.user.email,
        amount=order.total_price,
        reference=str(order.id)
    )

    if response.get("status"):
        return redirect(response["data"]["authorization_url"])

    messages.error(request, "Payment initialization failed")
    return redirect("orders:order_detail", order_id=order.id)
```

---

# 8. Payment Verification

```python id="view2"
import requests
from django.conf import settings


def verify_payment(reference):

    url = f"https://api.paystack.co/transaction/verify/{reference}"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    response = requests.get(url, headers=headers)
    return response.json()
```

---

# 9. Webhook Handler (Important)

Create:

`payments/views.py`

```python id="hook1"
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def paystack_webhook(request):

    payload = json.loads(request.body)

    event = payload.get("event")

    if event == "charge.success":

        reference = payload["data"]["reference"]

        # mark order as paid
        order = Order.objects.get(id=reference)
        order.status = "paid"
        order.save()

    return HttpResponse(status=200)
```

---

# 10. Order Model Requirement

Ensure your `Order` model includes:

```python id="mdl1"
status = models.CharField(
    max_length=20,
    choices=[
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ],
    default="pending"
)

reference = models.CharField(max_length=100, unique=True, null=True, blank=True)
```

---

# 11. URL Configuration

```python id="url1"
path("payments/pay/<int:order_id>/", views.pay_for_order, name="pay"),
path("payments/webhook/", views.paystack_webhook, name="webhook"),
```

---

# 12. Security Rules

* Never trust frontend payment success
* Always verify via Paystack API or webhook
* Always validate order ownership
* Always store transaction reference
* Never mark order as paid manually in production

---

# 13. Testing Flow

Use Paystack test mode:

* Test card numbers provided by Paystack
* Simulate webhook events
* Validate order status updates

---

# 14. Production Checklist

Before going live:

* Switch to live Paystack keys
* Enable HTTPS
* Configure webhook URL publicly
* Add logging for payment failures
* Test full checkout flow

---

# 15. Summary

Paystack becomes the financial backbone of LosTemplates.

Once implemented, your platform supports:

* Real payments
* Automatic order fulfillment
* Secure download unlocking
* Scalable monetization

---

# Revision History

| Version | Date      | Changes                             |
| ------- | --------- | ----------------------------------- |
| 0.3.0   | June 2026 | Initial Paystack integration design |
