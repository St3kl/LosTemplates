# 02_Database_Design.md

# LosTemplates Database Design

**Project:** LosTemplates

**Version:** 0.3.0

**Database Engine (Development):** SQLite

**Target Production Database:** PostgreSQL

---

# 1. Purpose

This document defines the database architecture for LosTemplates. It describes every model, relationship, constraint, and design decision used throughout the application.

The objective is to maintain a database that is secure, scalable, normalized, and easy to extend as the platform grows.

---

# 2. Database Overview

LosTemplates stores data for:

* Users
* Product categories
* Digital products
* Shopping carts
* Orders
* Purchased items

Each business domain is represented by a dedicated Django model.

---

# 3. Entity Relationship Diagram (ERD)

```text
+-----------+
|   User    |
+-----------+
      |
      | 1
      |
      | N
+-----------+
|   Order   |
+-----------+
      |
      | 1
      |
      | N
+--------------+
|  OrderItem   |
+--------------+
      |
      | N
      |
      | 1
+-----------+
|  Product  |
+-----------+
      |
      | N
      |
      | 1
+-----------+
| Category  |
+-----------+
```

---

# 4. Current Models

The system currently contains the following primary models:

* Category
* Product
* Order
* OrderItem
* User (Django built-in)

---

# 5. User Model

Current implementation uses Django's built-in authentication model.

Table:

```
auth_user
```

Important fields include:

| Field        | Type     | Description            |
| ------------ | -------- | ---------------------- |
| id           | Integer  | Primary key            |
| username     | String   | Login name             |
| password     | String   | Hashed password        |
| email        | String   | Email address          |
| first_name   | String   | Optional               |
| last_name    | String   | Optional               |
| is_staff     | Boolean  | Admin access           |
| is_superuser | Boolean  | Full permissions       |
| date_joined  | DateTime | Registration timestamp |

---

# 6. Category Model

Represents product classifications.

Example categories:

* HTML Templates
* Django Templates
* React Templates
* Admin Dashboards
* UI Kits

Fields:

| Field | Type      | Description             |
| ----- | --------- | ----------------------- |
| id    | Integer   | Primary key             |
| name  | CharField | Category name           |
| slug  | SlugField | URL-friendly identifier |

Relationships:

* One Category → Many Products

---

# 7. Product Model

Represents a digital product available for purchase.

Typical fields:

| Field             | Type                 |
| ----------------- | -------------------- |
| id                | Integer              |
| category          | ForeignKey(Category) |
| title             | CharField            |
| slug              | SlugField            |
| short_description | TextField            |
| description       | TextField            |
| price             | DecimalField         |
| thumbnail         | ImageField           |
| download_file     | FileField            |
| version           | CharField            |
| active            | Boolean              |
| created_at        | DateTime             |
| updated_at        | DateTime             |

Relationships:

* One Product belongs to one Category.
* One Product may appear in many OrderItems.

---

# 8. Order Model

Represents a customer's purchase.

Fields:

| Field       | Type             |
| ----------- | ---------------- |
| id          | Integer          |
| user        | ForeignKey(User) |
| status      | CharField        |
| total_price | DecimalField     |
| created_at  | DateTime         |
| updated_at  | DateTime         |

Status values may include:

* pending
* paid
* cancelled
* refunded

Relationships:

* One User → Many Orders
* One Order → Many OrderItems

---

# 9. OrderItem Model

Represents an individual product inside an order.

Fields:

| Field      | Type                |
| ---------- | ------------------- |
| id         | Integer             |
| order      | ForeignKey(Order)   |
| product    | ForeignKey(Product) |
| price      | DecimalField        |
| downloaded | Boolean             |

Relationships:

* Many OrderItems belong to one Order.
* Many OrderItems reference one Product.

---

# 10. Relationship Summary

```
Category
    │
    └──────► Product

User
    │
    └──────► Order

Order
    │
    └──────► OrderItem

Product
    │
    └──────► OrderItem
```

---

# 11. Primary Keys

Every model uses an auto-incrementing integer primary key.

Example:

```python
id = models.BigAutoField(primary_key=True)
```

This is Django's default configuration.

---

# 12. Foreign Keys

Current foreign key relationships include:

Product

```
category → Category
```

Order

```
user → User
```

OrderItem

```
order → Order
product → Product
```

---

# 13. Data Integrity

The database enforces integrity through:

* Primary keys
* Foreign keys
* Required fields
* Cascading deletes where appropriate
* Django ORM validation

---

# 14. Indexing Strategy

Indexes should exist on:

* username
* email
* slug
* created_at
* status

Additional indexes may be added as reporting and search requirements evolve.

---

# 15. Normalization

The database is designed according to Third Normal Form (3NF):

* No duplicated product information
* No duplicated customer information
* Orders separated from products
* Categories separated from products
* Purchased items stored independently

This minimizes redundancy and simplifies maintenance.

---

# 16. Migration Strategy

Database changes should always follow this workflow:

```bash
python manage.py makemigrations

python manage.py migrate
```

Every schema modification should be committed to version control with its corresponding migration file.

---

# 17. Future Tables

The following models are planned:

## Review

* Product rating
* User review
* Review date

---

## Wishlist

* User
* Product

---

## Coupon

* Discount code
* Percentage
* Expiration
* Active status

---

## Payment

* Order
* Transaction ID
* Provider
* Status
* Amount
* Currency

---

## Vendor

* Creator profile
* Bio
* Portfolio
* Revenue

---

## Notification

* User
* Message
* Read status
* Timestamp

---

## License

* Product
* License key
* Activation limit
* Expiration

---

## API Token

* User
* Access token
* Expiration
* Permissions

---

# 18. Production Database

Development uses SQLite for simplicity.

Production deployment will use PostgreSQL because it provides:

* Better concurrency
* Improved performance
* Advanced indexing
* JSON support
* Stronger reliability
* Better scalability
* Mature backup and replication options

---

# 19. Database Design Principles

The LosTemplates database follows these principles:

* Normalize data where practical
* Avoid unnecessary duplication
* Keep relationships explicit
* Prefer foreign keys over repeated values
* Preserve historical purchase data
* Design for future growth

---

# 20. Summary

The database architecture is intentionally modular and normalized to support the current digital marketplace while providing a clear path for future expansion into a multi-vendor, enterprise-ready platform.

---

# Revision History

| Version | Date      | Changes                               |
| ------- | --------- | ------------------------------------- |
| 0.3.0   | June 2026 | Initial database design documentation |
