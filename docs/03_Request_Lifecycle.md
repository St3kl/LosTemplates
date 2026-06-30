# 03_Request_Lifecycle.md

# LosTemplates Request Lifecycle

**Project:** LosTemplates

**Version:** 0.3.0

**Framework:** Django 5.x

---

# 1. Purpose

This document explains how an HTTP request travels through the LosTemplates application—from the moment a user interacts with the browser until a response is returned.

Understanding this lifecycle helps developers debug issues, optimize performance, and build new features with confidence.

---

# 2. High-Level Flow

Every request follows the same general path.

```text
Browser
   │
   ▼
Web Server
   │
   ▼
Django URL Dispatcher
   │
   ▼
View Function
   │
   ▼
Business Logic
   │
   ▼
Database (ORM)
   │
   ▼
Template Rendering
   │
   ▼
HTTP Response
   │
   ▼
Browser
```

---

# 3. Example Request

A visitor opens:

```text
/products/
```

The request flows as follows:

```text
Browser

↓

HTTP GET /products/

↓

config/urls.py

↓

apps/products/urls.py

↓

product_list()

↓

Product.objects.filter(active=True)

↓

Database

↓

products/product_list.html

↓

HTML Response

↓

Browser
```

---

# 4. URL Routing

Django receives the incoming URL and matches it against the project's URL configuration.

Example:

```python
path(
    "products/",
    include("apps.products.urls")
)
```

The request is then forwarded to the appropriate application.

---

# 5. Application Routing

Inside the application:

```python
path(
    "",
    views.product_list,
    name="product_list"
)
```

Django calls the associated view function.

---

# 6. View Execution

A view is responsible for:

* Receiving the request
* Validating input
* Loading data
* Executing business rules
* Returning a response

Example:

```python
def product_list(request):

    products = Product.objects.filter(active=True)

    return render(
        request,
        "products/product_list.html",
        {"products": products}
    )
```

---

# 7. Business Logic

Business logic defines how the application behaves.

Examples include:

* User authentication
* Cart management
* Checkout
* Download authorization
* Purchase validation
* Order creation

Business rules should remain inside views or dedicated service layers as the project grows.

---

# 8. ORM Interaction

The Django ORM converts Python code into SQL.

Example:

```python
Product.objects.filter(active=True)
```

Equivalent SQL:

```sql
SELECT *
FROM products_product
WHERE active = TRUE;
```

Developers interact with Python objects instead of writing SQL directly.

---

# 9. Database Response

The database returns matching records.

The ORM converts those records into Django model instances.

Example:

```python
products = QuerySet[
    Product,
    Product,
    Product
]
```

---

# 10. Template Rendering

Views pass data to templates.

Example:

```python
context = {
    "products": products
}
```

The template receives the context.

```django
{% for product in products %}

{{ product.title }}

{% endfor %}
```

Django generates the final HTML document.

---

# 11. HTTP Response

The rendered HTML is packaged into an HTTP response.

Example:

```python
return render(...)
```

The browser receives:

* HTML
* CSS references
* JavaScript references
* Images

---

# 12. Authentication Flow

Protected pages require authentication.

Example:

```python
@login_required
def dashboard(request):
```

Lifecycle:

```text
Request

↓

Authentication Middleware

↓

User Logged In?

├── Yes → Continue
└── No → Redirect to Login
```

---

# 13. Session Handling

LosTemplates stores temporary user information in sessions.

Examples:

* Logged-in user
* Shopping cart
* Flash messages

Example:

```python
request.session["cart"]
```

Sessions persist between requests until they expire or the user logs out.

---

# 14. Messages Framework

User notifications are stored using Django's messaging system.

Example:

```python
messages.success(
    request,
    "Product added successfully."
)
```

Flow:

```text
View

↓

Message Storage

↓

Redirect

↓

Template Displays Message
```

---

# 15. File Download Request

Example:

```text
/orders/download/15/
```

Processing steps:

```text
URL

↓

download_product()

↓

Validate Login

↓

Verify Ownership

↓

Locate File

↓

Return FileResponse

↓

Browser Downloads File
```

Unauthorized users receive a 404 or 403 response.

---

# 16. Shopping Cart Flow

```text
User Clicks Add to Cart

↓

POST Request

↓

add_to_cart()

↓

Update Session or Order

↓

Redirect

↓

Cart Page
```

---

# 17. Checkout Flow

```text
Shopping Cart

↓

Checkout View

↓

Validate Cart

↓

Create Order

↓

Create Order Items

↓

Calculate Total

↓

Save Order

↓

Clear Cart

↓

Success Page
```

---

# 18. Error Handling

Common errors include:

## 404

Requested resource not found.

Example:

```python
get_object_or_404()
```

---

## 403

Permission denied.

Used when users attempt to access unauthorized resources.

---

## 500

Internal server error.

Usually caused by:

* Programming errors
* Missing database fields
* Incorrect template syntax
* Missing URL patterns

---

# 19. Middleware Pipeline

Every request passes through middleware before reaching the view.

Typical sequence:

```text
Browser

↓

Security Middleware

↓

Session Middleware

↓

Authentication Middleware

↓

Message Middleware

↓

CSRF Middleware

↓

URL Resolver

↓

View
```

Middleware can inspect or modify requests and responses globally.

---

# 20. Request Types

LosTemplates currently uses:

### GET

Retrieve data.

Examples:

* Product list
* Product detail
* Dashboard

---

### POST

Submit data.

Examples:

* Login
* Registration
* Add to Cart
* Checkout
* Remove Item

Future versions may introduce PUT, PATCH, and DELETE for API endpoints.

---

# 21. Security Checks

Before executing sensitive actions, the application verifies:

* Authentication
* CSRF token
* Object ownership
* URL validity
* Database integrity

These checks help prevent unauthorized access and common web attacks.

---

# 22. Performance Considerations

To improve performance, the project uses or plans to use:

* `select_related()`
* `prefetch_related()`
* Database indexing
* Static file caching
* Browser caching
* CDN for media
* Query optimization

Avoid unnecessary database queries inside loops.

---

# 23. Request Lifecycle Summary

```text
Browser

↓

URL Dispatcher

↓

View

↓

Business Logic

↓

ORM

↓

Database

↓

Context

↓

Template

↓

HTTP Response

↓

Browser
```

---

# 24. Key Takeaways

* URLs determine which view executes.
* Views contain application logic.
* The ORM abstracts SQL queries.
* Templates render dynamic HTML.
* Middleware provides cross-cutting functionality.
* Sessions preserve user state.
* Authentication protects restricted resources.
* Responses are returned as standard HTTP responses.

---

# Revision History

| Version | Date      | Changes                                 |
| ------- | --------- | --------------------------------------- |
| 0.3.0   | June 2026 | Initial request lifecycle documentation |
