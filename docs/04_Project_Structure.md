# 04_Project_Structure.md

# LosTemplates Project Structure

**Project:** LosTemplates

**Version:** 0.3.0

**Framework:** Django 5.x

---

# 1. Purpose

This document describes the organization of the LosTemplates source code. It explains the purpose of every major directory, establishes coding conventions, and provides guidelines for adding new features without creating technical debt.

The primary goals are:

* Maintain a clean architecture
* Improve code discoverability
* Encourage consistency
* Support long-term scalability

---

# 2. Project Overview

Current high-level structure:

```text
LosTemplates/
│
├── apps/
├── config/
├── media/
├── static/
├── templates/
├── venv/
├── manage.py
├── requirements.txt
└── README.md
```

---

# 3. Root Directory

The project root contains everything required to run and manage the application.

### Example

```text
LosTemplates/
```

Contents include:

* Django applications
* Configuration
* Static assets
* Uploaded media
* Templates
* Virtual environment
* Documentation

---

# 4. apps/

```text
apps/
```

This directory contains every Django application.

Current applications include:

```text
apps/

accounts/
cart/
orders/
products/
```

Each application represents a single business domain.

---

# 5. accounts/

Responsible for:

* Registration
* Login
* Logout
* Dashboard
* Downloads
* User profile (future)

Typical structure:

```text
accounts/

models.py
views.py
urls.py
admin.py
forms.py
tests.py
```

---

# 6. products/

Responsible for:

* Categories
* Product listing
* Product detail
* Search
* Product download
* Product management

---

# 7. cart/

Responsible for:

* Shopping cart
* Add item
* Remove item
* Cart display
* Cart validation

---

# 8. orders/

Responsible for:

* Checkout
* Orders
* Purchases
* Download authorization
* Payment processing

---

# 9. config/

Contains Django configuration.

Example:

```text
config/

settings.py
urls.py
asgi.py
wsgi.py
```

Responsibilities:

* Installed apps
* Middleware
* Templates
* Static files
* Database
* Authentication
* URL routing

---

# 10. templates/

Contains HTML templates.

Example:

```text
templates/

base.html

products/
cart/
orders/
accounts/
```

Each application owns its own template folder.

Example:

```text
templates/products/

list.html
detail.html
```

---

# 11. static/

Stores frontend assets.

Example:

```text
static/

css/
js/
images/
fonts/
icons/
```

Example:

```text
static/css/style.css

static/js/main.js

static/images/logo.png
```

---

# 12. media/

Stores uploaded files.

Examples:

```text
media/

products/
avatars/
downloads/
```

Examples of uploaded content:

* Product thumbnails
* Downloadable ZIP files
* User avatars (future)

---

# 13. manage.py

Main project management script.

Common commands:

```bash
python manage.py runserver

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

python manage.py shell

python manage.py collectstatic
```

---

# 14. requirements.txt

Lists Python dependencies.

Example:

```text
Django
Pillow
gunicorn
whitenoise
psycopg
paystack
```

Future deployments should install dependencies using:

```bash
pip install -r requirements.txt
```

---

# 15. Naming Conventions

Applications

```text
accounts
products
orders
cart
```

Use lowercase.

---

Models

```text
Product

Category

Order

OrderItem
```

Use PascalCase.

---

Functions

```python
product_detail()

checkout()

download_product()
```

Use snake_case.

---

Variables

```python
product

order

items

total_price
```

Use descriptive snake_case names.

---

Template Files

```text
detail.html

list.html

dashboard.html

checkout.html
```

Use lowercase.

---

# 16. Import Organization

Recommended order:

```python
# Python Standard Library

import os

# Django Imports

from django.shortcuts import render

# Third-Party Packages

# Local Applications

from apps.products.models import Product
```

This improves readability and consistency.

---

# 17. Where New Features Go

Example:

Customer reviews

```text
apps/reviews/
```

Vendor marketplace

```text
apps/vendors/
```

Coupons

```text
apps/coupons/
```

Notifications

```text
apps/notifications/
```

Analytics

```text
apps/analytics/
```

Each major feature should live in its own Django application.

---

# 18. File Responsibilities

| File      | Responsibility             |
| --------- | -------------------------- |
| models.py | Database models            |
| views.py  | Business logic             |
| urls.py   | URL routing                |
| admin.py  | Django admin configuration |
| forms.py  | Forms and validation       |
| tests.py  | Automated tests            |
| apps.py   | Application configuration  |

---

# 19. Coding Standards

The project follows these principles:

* One responsibility per module
* Small, focused functions
* Clear variable names
* No duplicated logic
* Consistent formatting
* Meaningful comments only where necessary

---

# 20. Recommended Growth Structure

As the project expands, consider organizing each app like this:

```text
products/

models/
    product.py
    category.py

views/
    list.py
    detail.py
    download.py

services/

repositories/

validators/

tests/
```

This modular structure keeps large codebases manageable.

---

# 21. Documentation Directory

Create a dedicated documentation folder:

```text
docs/

01_Architecture.md
02_Database_Design.md
03_Request_Lifecycle.md
04_Project_Structure.md
```

Future documents will also be stored here.

---

# 22. Version Control

Recommended Git workflow:

* Feature branches for new functionality
* Small, focused commits
* Descriptive commit messages
* Pull requests for code review (if working in a team)

---

# 23. Future Directory Expansion

Planned additions:

```text
api/
docs/
scripts/
tests/
docker/
nginx/
.github/
```

These will support APIs, automation, deployment, testing, and continuous integration.

---

# 24. Summary

The LosTemplates project structure is organized around Django applications, with each app owning its models, views, templates, and business logic. This modular design promotes maintainability, scalability, and ease of collaboration as the platform evolves from a template marketplace into a full-featured digital commerce ecosystem.

---

# Revision History

| Version | Date      | Changes                                 |
| ------- | --------- | --------------------------------------- |
| 0.3.0   | June 2026 | Initial project structure documentation |
