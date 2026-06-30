# 09_Order_Lifecycle_Engine.md

# LosTemplates Order Lifecycle Engine

**Project:** LosTemplates
**Version:** 0.3.0
**Domain:** Commerce / Order Management System

---

# 1. Purpose

This document defines the full lifecycle of an order in LosTemplates.

It ensures:

* Predictable order behavior
* Secure access control
* Clean payment-to-download flow
* Fraud resistance
* Scalable SaaS logic

---

# 2. Order State Machine

Every order follows a strict state transition model:

```text id="state1"
PENDING → PAID → FULFILLED
    ↓         ↓
  FAILED   REFUNDED
```

---

# 3. State Definitions

## PENDING

Order created but not paid.

* User initiated checkout
* Payment not confirmed
* No download access

---

## PAID

Payment confirmed via Paystack.

* Payment verified (webhook/API)
* User gains entitlement
* Downloads unlocked

---

## FULFILLED

Final usable state.

* All items delivered
* Download tracked (optional analytics)
* System considers order complete

---

## FAILED

Payment failed or abandoned.

* No funds received
* No access granted
* Order may be retried

---

## REFUNDED

Payment reversed.

* Access revoked
* Downloads disabled (if enforced)
* Audit log required

---

# 4. Lifecycle Flow

```text id="flow2"
User adds product
        ↓
Order created (PENDING)
        ↓
User pays via Paystack
        ↓
Webhook confirms payment
        ↓
Order → PAID
        ↓
System unlocks downloads
        ↓
User downloads product
        ↓
Order → FULFILLED
```

---

# 5. Business Rules

## Rule 1 — Access Control

Only orders with:

```text id="rule1"
status = "paid"
```

can access downloads.

---

## Rule 2 — No Direct Trust

Never trust:

* Frontend “success” messages
* Redirect confirmations
* Client-side validation

Only backend verification matters.

---

## Rule 3 — One Payment → One Order

Each payment reference must map to a single order.

---

## Rule 4 — Immutable Paid Orders

Once `PAID`:

* Total price cannot change
* Items cannot be removed
* Order must be auditable

---

# 6. Entitlement System

When an order becomes PAID:

User automatically receives:

* Download permissions
* Product access rights

This is called an **entitlement grant**.

---

# 7. Download Authorization Logic

```python id="auth1"
def user_can_download(user, item):
    return (
        item.order.user == user and
        item.order.status == "paid"
    )
```

---

# 8. Order Fulfillment Strategy

Two options:

## Option A (Immediate Fulfillment)

* Order becomes FULFILLED after payment
* Simple model
* Recommended for digital products

## Option B (Tracked Fulfillment)

* FULFILLED after first download
* Better analytics
* More complex logic

---

# 9. Download Tracking (Optional Enhancement)

```python id="track1"
class OrderItem(models.Model):
    downloaded = models.BooleanField(default=False)
    downloaded_at = models.DateTimeField(null=True, blank=True)
```

Update on download:

* mark `downloaded = True`
* store timestamp

---

# 10. Security Rules

* Never expose raw file paths publicly
* Always validate ownership
* Always check order status
* Never allow cross-user downloads
* Validate item belongs to order

---

# 11. Anti-Fraud Layer (Basic)

Detect anomalies:

* multiple rapid downloads
* reused payment references
* mismatched user/order IDs

Future enhancement: fraud scoring system.

---

# 12. Error Handling Strategy

| Issue                | Response       |
| -------------------- | -------------- |
| Payment not verified | keep PENDING   |
| Invalid reference    | reject webhook |
| Missing file         | return 404     |
| Unauthorized access  | deny download  |

---

# 13. Database Integrity Rules

* Order → User (FK, required)
* OrderItem → Order (FK, cascade delete)
* Product → must remain immutable after purchase

---

# 14. Scaling Considerations

Future improvements:

* Redis caching for entitlement checks
* Background job processing (Celery)
* Webhook queue processing
* Audit logs for all state changes

---

# 15. Summary

This engine ensures:

* Orders behave predictably
* Payments are securely verified
* Downloads are properly controlled
* System is scalable to SaaS level

It is the backbone of monetization in LosTemplates.

---

# Revision History

| Version | Date      | Changes                               |
| ------- | --------- | ------------------------------------- |
| 0.3.0   | June 2026 | Initial order lifecycle engine design |

