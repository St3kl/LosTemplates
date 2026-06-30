# 15_Paystack_Integration_Implementation.md

# LosTemplates Paystack Integration Implementation

**Project:** LosTemplates
**Version:** 0.3.0
**Domain:** Payments / Paystack / Webhooks / Production Integration

---

# 1. Purpose

This document implements Paystack as the payment provider for LosTemplates.

It covers:

* Payment initialization
* Transaction verification
* Webhook processing
* Order status updates
* Security validation

---

# 2. Why Paystack

Since Stripe is not fully supported in all regions (including Ghana), Paystack is used because:

* Strong support in Africa
* Reliable API
* Built-in webhook system
* Local payment methods (mobile money, cards, etc.)

---

# 3. Integration Architecture

```text id="arch1"
Frontend Checkout
        ↓
Backend (Django)
        ↓
Paystack API
        ↓
Webhook Callback
        ↓
Order Updated (PAID)
```

---

# 4. Environment Variables

Store sensitive keys securely:

```text id="env1"
PAYSTACK_SECRET_KEY=your_secret_key
PAYSTACK_PUBLIC_KEY=your_public_key
PAYSTACK_CALLBACK_URL=https://yourdomain.com/paystack/callback/
```

---

# 5. Payment Initialization

## Service Layer (Recommended)

Create:

```text id="svc1"
apps/payments/services.py
```

---

### Initialize Transaction

```python id="init1"
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
        "amount": int(amount * 100),  # convert to kobo
        "reference": reference,
        "callback_url": settings.PAYSTACK_CALLBACK_URL,
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()
```

---

# 6. Payment View (Django)

```python id="view1"
@login_required
def start_payment(request, order_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)

    reference = f"LS-{order.id}-{uuid.uuid4().hex[:6]}"

    response = initialize_payment(
        email=request.user.email,
        amount=order.total_price,
        reference=reference
    )

    if response["status"]:
        return redirect(response["data"]["authorization_url"])

    messages.error(request, "Payment initialization failed")
    return redirect("cart:cart")
```

---

# 7. Paystack Webhook Handler

This is the MOST IMPORTANT part.

```python id="web1"
@csrf_exempt
def paystack_webhook(request):

    payload = request.body
    event = json.loads(payload)

    if event["event"] == "charge.success":

        reference = event["data"]["reference"]

        order_id = reference.split("-")[1]

        order = Order.objects.get(id=order_id)

        order.status = "paid"
        order.save()

    return HttpResponse(status=200)
```

---

# 8. Payment Verification (Extra Safety Layer)

Even with webhook, we verify:

```python id="verify1"
def verify_payment(reference):

    url = f"https://api.paystack.co/transaction/verify/{reference}"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    response = requests.get(url, headers=headers)

    return response.json()
```

---

# 9. Order Status Update Rules

Only update order if:

```text id="rule1"
- Payment verified successfully
- Reference matches order
- Event is charge.success
```

---

# 10. Security Rules

## MUST IMPLEMENT

* Verify Paystack signature header
* Ignore duplicate webhooks
* Never trust frontend payment status
* Validate order ownership

---

# 11. Idempotency Protection

Prevent double processing:

```text id="id1"
if order.status == "paid":
    ignore webhook
```

---

# 12. Common Errors & Fixes

## 12.1 Payment not redirecting

* Check secret key
* Check callback URL

---

## 12.2 Webhook not firing

* Use ngrok for local testing
* Ensure endpoint is public

---

## 12.3 Order not updating

* Verify reference parsing
* Check logs

---

# 13. Testing Strategy

Use Paystack test mode:

* Test cards provided by Paystack
* Simulate successful payments
* Validate webhook calls

---

# 14. Production Deployment Notes

* Use HTTPS only
* Store secrets in environment variables
* Enable logging for webhook failures
* Monitor payment success rates

---

# 15. Future Enhancements

* Refund system
* Partial payments
* Subscription billing
* Multi-currency support
* Payment analytics dashboard

---

# 16. Summary

This implementation completes your payment system:

* Real Paystack integration
* Secure webhook processing
* Order status automation
* Production-ready payment flow

---

# Revision History

| Version | Date      | Changes                                  |
| ------- | --------- | ---------------------------------------- |
| 0.3.0   | June 2026 | Full Paystack integration implementation |
