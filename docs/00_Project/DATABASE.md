# DATABASE.md

**Document Version:** 1.0.0

**Project Version:** 0.8.0

**Database Engine (Development):** SQLite

**Database Engine (Production):** PostgreSQL (Planned)

**Last Updated:** 2026-06-27

---

# Purpose

This document defines the complete database architecture of LosTemplates.

It describes:

- Entity relationships
- Database models
- Constraints
- Business rules
- Data integrity
- Future schema evolution

This document should allow a developer to recreate the database without reading the Django models.

---

# Database Philosophy

The database follows these principles:

- Normalized structure
- Minimal data duplication
- Strong relationships
- Clear ownership
- Referential integrity
- Scalability
- Security

The application is designed around relational data.

---

# Entity Relationship Diagram (Current)

                    User
                      │
                      │
                 1 ───┼──── N
                      │
                    Order
                      │
                      │
                 N ───┼──── 1
                      │
                   Product
                      │
          ┌───────────┴────────────┐
          │                        │
      N   │                    1   │
          ▼                        ▼
   ProductImage               Category

---

# Current Models

1. User
2. Category
3. Product
4. ProductImage
5. Order

---

# Model Specification

----------------------------------------------------
User
----------------------------------------------------

Source:

Django Authentication System

Purpose:

Represents registered customers.

Primary Key

id

Relationships

One User

↓

Many Orders

Future Relationships

Wishlist

Reviews

Download History

Notifications

Roles

---

----------------------------------------------------
Category
----------------------------------------------------

Purpose

Groups similar products.

Fields

id

Primary Key

name

String

Unique

slug

Unique

Used for URLs

description

Text

Optional

created_at

Timestamp

Relationships

One Category

↓

Many Products

Business Rules

Category names must be unique.

Every Product belongs to exactly one Category.

Example

Website Templates

Dashboard Templates

Excel Templates

PowerPoint Templates

---

----------------------------------------------------
Product
----------------------------------------------------

Purpose

Represents a downloadable product.

Fields

id

Primary Key

category

Foreign Key

title

String

slug

Unique

short_description

String

description

Text

price

Decimal

thumbnail

Image

download_file

File

file_size_mb

Decimal

Optional

version

String

featured

Boolean

active

Boolean

created_at

Timestamp

updated_at

Timestamp

Relationships

Many Products

↓

One Category

One Product

↓

Many Product Images

One Product

↓

Many Orders

Business Rules

Slug must be unique.

Price cannot be negative.

Inactive products cannot be displayed.

Every product belongs to exactly one category.

Download file is required.

Thumbnail is required.

Example

Title

Modern SaaS Dashboard

Price

29.00

Version

1.0.0

Featured

True

---

----------------------------------------------------
ProductImage
----------------------------------------------------

Purpose

Stores additional screenshots.

Fields

id

Primary Key

product

Foreign Key

image

Image

alt_text

String

display_order

Integer

Relationships

Many Images

↓

One Product

Business Rules

Images belong to only one product.

Display order controls gallery sequence.

---

----------------------------------------------------
Order
----------------------------------------------------

Purpose

Represents a purchase.

Fields

(Current implementation may evolve.)

Typical Fields

id

user

product

purchase_date

status

download_count

license_key

Relationships

Many Orders

↓

One User

Many Orders

↓

One Product

Business Rules

Only completed orders grant download permission.

One order belongs to one user.

One order references one product.

Future Stripe payment IDs will be stored here.

---

# Relationship Summary

User

1

↓

N

Order

Order

N

↓

1

Product

Category

1

↓

N

Product

Product

1

↓

N

ProductImage

---

# Data Integrity Rules

Rule 001

Products must always reference an existing category.

Rule 002

Product images must always reference an existing product.

Rule 003

Orders must reference an existing user.

Rule 004

Orders must reference an existing product.

Rule 005

Deleting a category deletes its products.

Rule 006

Deleting a product deletes its gallery.

Rule 007

Deleting a product deletes related orders only if explicitly configured.

---

# Indexing Strategy

Current

Primary Keys

Unique Slugs

Future

Index

Product.active

Index

Product.featured

Index

Product.created_at

Index

Category.slug

Index

Order.user

Index

Order.purchase_date

Composite indexes may be introduced as search complexity grows.

---

# Naming Conventions

Tables

Singular Django Models

Category

Product

Order

Fields

snake_case

Foreign Keys

Singular

Example

category

user

product

---

# Future Models

Cart

Stores shopping carts.

CartItem

Stores products inside carts.

Review

Stores customer reviews.

Wishlist

Stores favorite products.

Coupon

Stores discounts.

License

Stores software licenses.

DownloadHistory

Stores download logs.

Notification

Stores system notifications.

Payment

Stores Stripe transaction metadata.

---

# Future Database Evolution

Version 0.9

Cart

CartItem

Version 1.0

Stripe

Payment

License

DownloadHistory

Version 2.0

Reviews

Wishlist

Coupons

Search Analytics

---

# Database Security

Never trust client-side data.

All ownership checks happen on the server.

Downloads require:

Authentication

+

Ownership

Future improvements:

Encrypted backups

Signed URLs

Audit logs

Role permissions

Rate limiting

---

# Backup Strategy

Development

Manual backups.

Production

Automated PostgreSQL backups.

Daily snapshots.

Off-site storage.

Disaster recovery plan.

---

# Database Principles

The database should remain:

- Normalized
- Consistent
- Secure
- Scalable
- Easy to maintain

Data integrity always has higher priority than convenience.

---

# End of Document

This document must remain synchronized with every database migration.

Whenever a model changes, DATABASE.md must be updated before the phase is considered complete.