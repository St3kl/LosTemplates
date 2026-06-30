# 10_Security_and_Access_Control.md

# LosTemplates Security & Access Control Guide

**Project:** LosTemplates
**Version:** 0.3.0
**Domain:** Security / Authorization Layer

---

# 1. Purpose

This document defines how access is controlled across the entire LosTemplates system.

It ensures:

* Only authorized users can access paid content
* Files cannot be leaked or bypassed
* Views are protected consistently
* Business rules are enforced at backend level

---

# 2. Core Security Principle

## NEVER TRUST THE CLIENT

All security decisions must be enforced:

* In Django views
* In middleware (if needed)
* In backend services

Not in templates or frontend logic.

---

# 3. Access Control Levels

## Level 1 — Public Access

No authentication required:

* Product listing
* Product details
* Landing pages

---

## Level 2 — Authenticated Users

Requires login:

* Cart
* Checkout
* Dashboard
* Order history

---

## Level 3 — Paid Access

Requires:

```text id="acl1"
order.status == "paid"
```

Allows:

* File downloads
* Premium content access

---

# 4. Download Security Model

Every download must pass:

```text id="sec1"
1. User is authenticated
2. Order belongs to user
3. Order is PAID
4. Item belongs to order
5. File exists on server
```

---

# 5. Secure Download Pattern

Always use backend validation:

```python id="dl1"
@login_required
def download_product(request, item_id):

    item = get_object_or_404(OrderItem, id=item_id)

    if item.order.user != request.user:
        raise Http404()

    if item.order.status != "paid":
        raise Http404()

    file_path = item.product.download_file.path
```

---

# 6. Template Security Rules

## NEVER do this:

```text id="bad1"
{% url 'download' product.slug %}
```

Without validating:

* ownership
* payment status
* item existence

---

## ALWAYS ensure:

```text id="good1"
item.product EXISTS
item.order.status == "paid"
```

---

# 7. Object Ownership Rule

A user can ONLY access:

* Their own orders
* Their own order items
* Their own downloads

Enforced via:

```python id="own1"
filter(user=request.user)
```

---

# 8. URL Protection Strategy

All sensitive routes must include:

* Login protection
* Object validation

Example:

```python id="urlsec"
@login_required
def view(request, id):
    ...
```

---

# 9. Anti-Bypass Protection

Prevent:

* Guessing download URLs
* Direct file access
* ID enumeration attacks

Solution:

* Always check ownership
* Never expose file paths directly
* Use Django FileResponse only after validation

---

# 10. File System Security

Rules:

* Files must NOT be inside publicly browsable folders
* Media access must be controlled via Django
* No direct `/media/` exposure for paid files

---

# 11. Session Security (Cart)

Cart rules:

* Cart stored in session only
* No sensitive data stored in frontend
* Server validates product IDs

---

# 12. Admin vs User Separation

| Area        | Access          |
| ----------- | --------------- |
| Admin panel | Staff only      |
| Orders      | User-specific   |
| Downloads   | Ownership-based |

---

# 13. Error Handling Strategy

| Attack / Issue      | Response                                 |
| ------------------- | ---------------------------------------- |
| Unauthorized access | 404 (not 403 to hide resource existence) |
| Invalid item ID     | 404                                      |
| Missing file        | 404                                      |
| Unpaid order        | 404                                      |

---

# 14. Logging (Recommended Upgrade)

Log sensitive events:

* Failed download attempts
* Unauthorized access attempts
* Payment mismatches

Future integration: Django logging + monitoring system

---

# 15. Future Enhancements

* JWT-based API security layer
* Rate limiting on downloads
* IP-based abuse detection
* Watermarking downloaded files
* Encrypted file storage

---

# 16. Summary

Security in LosTemplates is based on one rule:

> Every access must be verified, never assumed.

This ensures:

* No unauthorized downloads
* No payment bypass
* No data leaks
* Production-grade SaaS safety

---

# Revision History

| Version | Date      | Changes                                    |
| ------- | --------- | ------------------------------------------ |
| 0.3.0   | June 2026 | Initial security and access control design |
