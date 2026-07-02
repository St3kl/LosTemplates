# 04 – Paystack Webhook Architecture

## Overview

The Paystack webhook system is the authoritative source of payment confirmation within LosTemplates.

While Paystack redirects users back to the application after payment, the redirect alone must never be trusted as proof of a successful transaction. Instead, the application relies on Paystack's server-to-server webhook notifications to verify and finalize payments securely.

---

# Objectives

The webhook system is responsible for:

* Verifying webhook authenticity.
* Processing successful payment events.
* Preventing duplicate payment processing.
* Updating payment records.
* Marking orders as paid.
* Unlocking purchased digital products.
* Recording webhook activity for auditing and debugging.

---

# Architecture

```
Customer
    │
    ▼
Paystack Checkout
    │
    ├──────────────► Redirect to Callback URL
    │
    └──────────────► Secure Webhook
                         │
                         ▼
                verify_paystack_signature()
                         │
                         ▼
                  process_webhook()
                         │
                         ▼
              Payment & Order Database
                         │
                         ▼
              Unlock Purchased Products
```

---

# Components

## views.py

Responsible for:

* Receiving incoming HTTP requests.
* Validating webhook requests.
* Passing verified payloads to the webhook processor.
* Returning appropriate HTTP responses.

Business logic should remain minimal within this file.

---

## utils.py

Responsible for:

* Verifying the `x-paystack-signature` header.
* Comparing HMAC SHA-512 signatures.
* Rejecting unauthorized webhook requests.

---

## webhooks.py

Responsible for:

* Processing Paystack events.
* Executing payment business logic.
* Updating payment records.
* Updating order status.
* Triggering download access.

---

## services.py

Responsible for:

* Initializing transactions.
* Verifying transaction references.
* Communicating with the Paystack API.

---

# Planned Supported Events

## charge.success

Marks a payment as successful and unlocks purchased products.

## charge.failed

Records failed payment attempts.

## refund.processed

Updates payment status after a refund.

## transfer.success

Reserved for future seller payouts.

---

# Security

The webhook endpoint must:

* Accept only POST requests.
* Verify every request signature.
* Reject invalid signatures.
* Process each transaction reference only once.
* Never trust client-side redirects.

---

# Future Enhancements

* Webhook event logging
* Retry-safe processing
* Idempotency protection
* Background job processing
* Email notifications
* Invoice generation
* Fraud detection
* Monitoring dashboard

---

# Development Status

| Component                  | Status     |
| -------------------------- | ---------- |
| Transaction Initialization | ✅ Complete |
| Callback Verification      | ✅ Complete |
| Webhook Endpoint           | 🟡 Basic   |
| Signature Verification     | ⏳ Next     |
| Event Processing           | ⏳ Next     |
| Idempotency Protection     | ⏳ Planned  |
| Download Unlocking         | ⏳ Planned  |
| Audit Logging              | ⏳ Planned  |

---

This document defines the foundation of the payment processing architecture for LosTemplates. All future payment gateways should follow the same layered design to maintain consistency, security, and maintainability.



# Idempotency & Payment Safety Layer

## Overview

To ensure production-grade reliability, the Paystack webhook system implements idempotency protection. This prevents duplicate processing of the same transaction reference, which can occur due to Paystack retrying webhook events.

---

## Problem Addressed

Paystack may send the same webhook event multiple times:

* Network retries
* Timeout retries
* Event re-delivery

Without protection, this can lead to:

* Duplicate payment confirmation
* Multiple order updates
* Inconsistent transaction state
* Security vulnerabilities in download access

---

## Solution: Idempotency Guard

The system ensures that each payment reference is processed only once.

### Implementation Strategy

1. Fetch payment using unique reference.
2. Check current payment status.
3. If status is already "success", ignore the request.
4. Use database locking (`select_for_update`) to prevent race conditions.
5. Ensure order status is updated only once.

---

## Safety Rules

* A payment reference must never be processed more than once.
* Webhook retries must be safe and ignored if already processed.
* Order updates must be conditional (only if not already paid).

---

## Updated Processing Flow

```text
Webhook Received
      ↓
Signature Verified
      ↓
Event Routed
      ↓
Idempotency Check
      ↓
Payment Updated (if new)
      ↓
Order Marked Paid (if needed)
      ↓
Access Granted
```

---

## Result

This ensures:

* ✔ Safe retry handling
* ✔ No duplicate payments
* ✔ Stable order state
* ✔ Production-ready reliability
