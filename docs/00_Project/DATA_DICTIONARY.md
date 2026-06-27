# DATA_DICTIONARY.md

Document Version: 1.0.0

Project Version: 0.8.0

Last Updated: 2026-06-27

---

# Purpose

The Data Dictionary defines every piece of data stored within the LosTemplates database.

Unlike DATABASE.md, which focuses on relationships and architecture, this document focuses on individual fields.

For every field, this document specifies:

- Data Type
- Required Status
- Default Value
- Validation Rules
- Business Meaning
- Example Value

This document should be updated whenever a database model changes.

---

# Data Standards

## Naming Convention

Database fields use:

snake_case

Example

created_at

download_file

short_description

---

## Primary Keys

All tables use:

id

Automatically generated.

---

## Foreign Keys

Foreign keys use singular names.

Examples:

category

product

user

order

---

## Timestamp Fields

Standard timestamp fields:

created_at

updated_at

Both use UTC internally.

---

# Category

## id

| Property | Value |
|----------|-------|
| Type | Integer |
| Required | Yes |
| Unique | Yes |
| Nullable | No |
| Description | Primary key |
| Example | 12 |

---

## name

| Property | Value |
|----------|-------|
| Type | CharField |
| Max Length | 100 |
| Required | Yes |
| Unique | Yes |
| Description | Category name |
| Example | Website Templates |

---

## slug

| Property | Value |
|----------|-------|
| Type | SlugField |
| Required | Yes |
| Unique | Yes |
| Description | URL-friendly identifier |
| Example | website-templates |

---

## description

| Property | Value |
|----------|-------|
| Type | TextField |
| Required | No |
| Default | Empty |
| Description | Category description |

---

## created_at

| Property | Value |
|----------|-------|
| Type | DateTime |
| Required | Yes |
| Auto Generated | Yes |
| Description | Creation timestamp |

---

# Product

## id

| Property | Value |
|----------|-------|
| Type | Integer |
| Required | Yes |
| Description | Primary key |

---

## category

| Property | Value |
|----------|-------|
| Type | ForeignKey |
| Required | Yes |
| References | Category |
| Description | Product category |

---

## title

| Property | Value |
|----------|-------|
| Type | CharField |
| Max Length | 255 |
| Required | Yes |
| Description | Product title |
| Example | Modern SaaS Dashboard |

---

## slug

| Property | Value |
|----------|-------|
| Type | SlugField |
| Unique | Yes |
| Required | Yes |
| Description | SEO-friendly URL |

---

## short_description

| Property | Value |
|----------|-------|
| Type | CharField |
| Max Length | 500 |
| Required | Yes |
| Description | Short product summary |

---

## description

| Property | Value |
|----------|-------|
| Type | TextField |
| Required | Yes |
| Description | Full product description |

---

## price

| Property | Value |
|----------|-------|
| Type | DecimalField |
| Precision | 10,2 |
| Required | Yes |
| Minimum | 0.00 |
| Description | Product selling price |

---

## thumbnail

| Property | Value |
|----------|-------|
| Type | ImageField |
| Required | Yes |
| Upload Path | thumbnails/ |
| Description | Product cover image |

---

## download_file

| Property | Value |
|----------|-------|
| Type | FileField |
| Required | Yes |
| Upload Path | products/ |
| Description | Downloadable source package |

---

## file_size_mb

| Property | Value |
|----------|-------|
| Type | DecimalField |
| Nullable | Yes |
| Description | File size in MB |

---

## version

| Property | Value |
|----------|-------|
| Type | CharField |
| Max Length | 20 |
| Default | 1.0.0 |
| Description | Product version |

---

## featured

| Property | Value |
|----------|-------|
| Type | Boolean |
| Default | False |
| Description | Featured on homepage |

---

## active

| Property | Value |
|----------|-------|
| Type | Boolean |
| Default | True |
| Description | Product visibility |

---

## created_at

| Property | Value |
|----------|-------|
| Type | DateTime |
| Auto Generated | Yes |
| Description | Product creation date |

---

## updated_at

| Property | Value |
|----------|-------|
| Type | DateTime |
| Auto Updated | Yes |
| Description | Last modification date |

---

# ProductImage

## id

| Property | Value |
|----------|-------|
| Type | Integer |
| Required | Yes |
| Description | Primary key |

---

## product

| Property | Value |
|----------|-------|
| Type | ForeignKey |
| Required | Yes |
| References | Product |
| Description | Related product |

---

## image

| Property | Value |
|----------|-------|
| Type | ImageField |
| Required | Yes |
| Upload Path | product_gallery/ |
| Description | Gallery screenshot |

---

## alt_text

| Property | Value |
|----------|-------|
| Type | CharField |
| Max Length | 255 |
| Required | No |
| Description | Accessibility text |

---

## display_order

| Property | Value |
|----------|-------|
| Type | PositiveInteger |
| Default | 0 |
| Description | Gallery display sequence |

---

# Order

> **Note:** The Order model is expected to evolve during future phases. This section documents the intended design and should be synchronized with implementation changes.

## id

| Property | Value |
|----------|-------|
| Type | Integer |
| Description | Primary key |

---

## user

| Property | Value |
|----------|-------|
| Type | ForeignKey |
| References | User |
| Required | Yes |
| Description | Customer who purchased the product |

---

## product

| Property | Value |
|----------|-------|
| Type | ForeignKey |
| References | Product |
| Required | Yes |
| Description | Purchased product |

---

## purchase_date

| Property | Value |
|----------|-------|
| Type | DateTime |
| Description | Date of purchase |

---

## status

| Property | Value |
|----------|-------|
| Type | CharField |
| Example Values | Pending, Paid, Refunded |
| Description | Order state |

---

## download_count

| Property | Value |
|----------|-------|
| Type | Integer |
| Default | 0 |
| Description | Number of downloads |

---

## license_key

| Property | Value |
|----------|-------|
| Type | CharField |
| Nullable | Yes |
| Description | Product license |

---

# Global Validation Rules

The following rules apply across the database:

- Prices cannot be negative.
- Slugs must be unique.
- Titles cannot be empty.
- Product images require a valid product.
- Orders require an existing user.
- Orders require an existing product.
- Every product belongs to one category.
- Every downloadable product must include a downloadable file.

---

# Reserved Fields

Future models should use these standard fields whenever appropriate:

created_at

updated_at

created_by

updated_by

deleted_at (Soft Delete)

is_active

---

# Data Integrity Checklist

Before every release verify:

☐ No nullable primary keys

☐ Unique slugs

☐ Valid foreign keys

☐ No orphan records

☐ No duplicate categories

☐ No inactive products shown publicly

☐ Download files exist

☐ Thumbnail images exist

---

# Future Expansion

Future versions of this document will include:

- Enumerations
- Validation regex
- Default values
- PostgreSQL data types
- Constraints
- Triggers
- Generated columns
- Audit fields

---

# End of Document

The Data Dictionary is the authoritative reference for every field stored in the LosTemplates database.