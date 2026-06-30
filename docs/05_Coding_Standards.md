# 05_Coding_Standards.md

# LosTemplates Coding Standards

**Project:** LosTemplates

**Version:** 0.3.0

**Framework:** Django 5.x

---

# 1. Purpose

This document defines the coding standards for the LosTemplates project.

The objectives are to:

* Maintain a consistent codebase
* Improve readability
* Simplify maintenance
* Reduce bugs
* Make collaboration easier
* Prepare the project for long-term growth

Every contributor should follow these guidelines.

---

# 2. General Principles

Write code that is:

* Simple
* Readable
* Consistent
* Maintainable
* Testable
* Secure

Prefer clarity over cleverness.

Good code is easier to understand than it is to write.

---

# 3. Python Style

Follow **PEP 8**.

Examples:

### Correct

```python
product = Product.objects.get(id=product_id)

total_price = 0
```

### Avoid

```python
p=Product.objects.get(id=id)

tp=0
```

Variable names should describe their purpose.

---

# 4. Naming Conventions

## Classes

Use PascalCase.

```python
Product

Category

Order

OrderItem
```

---

## Functions

Use snake_case.

```python
product_detail()

checkout()

download_product()
```

---

## Variables

```python
product

cart_items

order_total

current_user
```

Avoid abbreviations unless they are widely understood.

---

## Constants

Use uppercase.

```python
MAX_UPLOAD_SIZE = 50

DEFAULT_PAGE_SIZE = 20
```

---

# 5. File Organization

Each Django app should contain:

```text
models.py

views.py

urls.py

admin.py

forms.py

tests.py
```

As an app grows, split large modules into packages.

Example:

```text
views/

list.py
detail.py
download.py
checkout.py
```

---

# 6. Import Order

Imports should follow this order:

```python
# Standard library

import os

# Django

from django.shortcuts import render

# Third-party packages

# Local applications

from apps.products.models import Product
```

Separate groups with a blank line.

---

# 7. Functions

Functions should have one responsibility.

Good:

```python
def calculate_total(items):
```

Avoid:

```python
def calculate_total_send_email_save_database():
```

Small functions are easier to test and reuse.

---

# 8. Views

Views should:

* Validate input
* Retrieve data
* Apply business rules
* Return a response

Avoid placing unrelated logic in a single view.

Move reusable business logic into service modules as the project grows.

---

# 9. Models

Models represent business entities.

Example:

```python
class Product(models.Model):

    title = models.CharField(...)

    price = models.DecimalField(...)
```

Do not place presentation logic inside models.

---

# 10. Templates

Templates should only display data.

Good:

```django
{{ product.title }}
```

Avoid:

Complex calculations inside templates.

Business logic belongs in Python.

---

# 11. HTML Standards

Use semantic HTML whenever possible.

Preferred elements:

```html
<header>

<nav>

<main>

<section>

<article>

<footer>
```

Avoid unnecessary nested `<div>` elements.

Indent consistently.

---

# 12. CSS Standards

Organize CSS logically.

Example:

```css
/* Layout */

/* Navigation */

/* Cards */

/* Buttons */

/* Forms */

/* Responsive */
```

Use descriptive class names.

Good:

```css
.product-card

.download-button

.checkout-summary
```

Avoid names such as:

```css
.box1

.red

.bigDiv
```

---

# 13. JavaScript Standards

Use meaningful names.

```javascript
function addToCart(productId)
```

Avoid:

```javascript
function a(x)
```

Keep functions focused.

Avoid global variables whenever possible.

---

# 14. Comments

Write comments that explain **why**, not **what**.

Good:

```python
# Prevent duplicate purchases
```

Avoid:

```python
# Set variable to zero
total = 0
```

The code already explains what is happening.

---

# 15. Error Handling

Handle expected failures gracefully.

Example:

```python
product = get_object_or_404(
    Product,
    slug=slug
)
```

Avoid exposing internal errors to users.

Log unexpected exceptions for debugging.

---

# 16. Security

Always:

* Validate user input
* Use CSRF protection
* Protect authenticated views
* Verify object ownership
* Escape template output (Django does this by default)

Never trust client-side data.

---

# 17. Database Queries

Prefer efficient queries.

Good:

```python
.select_related()

.prefetch_related()
```

Avoid unnecessary queries inside loops.

---

# 18. Logging

Log important events.

Examples:

* Login failures
* Payment events
* Download attempts
* Exceptions

Avoid logging sensitive information such as passwords or payment details.

---

# 19. Git Commit Standards

Commit messages should be concise and descriptive.

Examples:

```text
feat: implement Paystack checkout

fix: resolve duplicate order creation

refactor: simplify dashboard queries

docs: add request lifecycle documentation

style: improve cart template formatting
```

One logical change per commit whenever possible.

---

# 20. Testing

Every major feature should include tests.

Focus on:

* Models
* Views
* Forms
* Permissions
* Business logic

Aim for repeatable and reliable tests.

---

# 21. Documentation

Document:

* New features
* APIs
* Configuration changes
* Database schema updates
* Deployment steps

Documentation should evolve alongside the codebase.

---

# 22. Performance

Optimize only after measuring.

Use:

* Query optimization
* Pagination
* Caching
* Lazy loading
* Efficient database indexing

Avoid premature optimization.

---

# 23. Accessibility

Follow basic accessibility practices.

* Use descriptive labels
* Include image alt text
* Ensure sufficient color contrast
* Support keyboard navigation
* Use semantic HTML

Accessibility improves usability for all users.

---

# 24. Code Review Checklist

Before merging code, verify:

* Follows project standards
* No duplicated logic
* No unnecessary complexity
* Proper error handling
* Security considerations addressed
* Documentation updated
* Tests added or updated
* Code formatted consistently

---

# 25. Summary

LosTemplates coding standards emphasize readability, consistency, security, and maintainability. Adhering to these practices ensures the codebase remains scalable as the project grows and as new contributors join the development effort.

---

# Revision History

| Version | Date      | Changes                           |
| ------- | --------- | --------------------------------- |
| 0.3.0   | June 2026 | Initial coding standards handbook |
