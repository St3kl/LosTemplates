# ARCHITECTURE.md

**Document Version:** 1.0.0

**Project Version:** 0.8.0

**Architecture Style:** Modular Monolith (Django)

**Last Updated:** 2026-06-27

---

# Purpose

This document defines the overall architecture of the LosTemplates application.

It explains how the system is organized, how components interact, and which architectural principles guide development.

This document is the primary technical reference for future development and architectural decisions.

---

# System Overview

LosTemplates is a **Single-Vendor Digital Marketplace** built using Django.

The application allows authenticated users to browse, purchase, and securely download digital products.

The current architecture follows a **Modular Monolith** approach.

Each Django application represents one business domain while remaining part of a single deployable project.

---

# High-Level Architecture

```text
                        Internet
                            │
                            ▼
                    Django Development Server
                            │
                            ▼
                    config (Project Layer)
                            │
        ┌───────────────────┼────────────────────┐
        ▼                   ▼                    ▼
     accounts            products             core
        │                   │                    │
        └───────────────┬───┘                    │
                        ▼                        ▼
                     orders                 Templates
                        │
                        ▼
                    SQLite Database
                        │
                        ▼
                   Media File Storage
```

---

# Architecture Style

Current Architecture:

Modular Monolith

Reason:

* Easier development
* Easier deployment
* Simple communication between apps
* Ideal for a growing Django application

Future Possibility:

If the project grows significantly, some domains may later become independent services.

Current roadmap does **not** include microservices.

---

# Layered Architecture

The application follows a layered design.

```text
Presentation Layer

Templates

Bootstrap

HTML

JavaScript

──────────────

Application Layer

Views

Forms (planned)

Services (planned)

──────────────

Domain Layer

Models

Business Rules

Managers (planned)

──────────────

Infrastructure Layer

SQLite

PostgreSQL (future)

Media Storage

Authentication

File System
```

Each layer has a specific responsibility.

---

# Django Apps

## config

Purpose:

Project configuration.

Responsibilities:

* Settings
* Root URLs
* WSGI
* ASGI

---

## core

Purpose:

Public website pages.

Responsibilities:

* Homepage
* Static pages
* Landing pages

Should not contain business logic.

---

## accounts

Purpose:

Authentication and user management.

Responsibilities:

* Login
* Logout
* Registration
* Dashboard
* User profile (future)

---

## products

Purpose:

Product catalog.

Responsibilities:

* Categories
* Products
* Galleries
* Product pages
* Secure downloads

---

## orders

Purpose:

Purchase management.

Responsibilities:

* Purchase records
* Ownership
* Download authorization

---

# Request Lifecycle

Example:

Product Detail Page

```text
Browser

↓

HTTP Request

↓

config/urls.py

↓

products/urls.py

↓

Product View

↓

Product Model

↓

SQLite

↓

Template Rendering

↓

HTTP Response

↓

Browser
```

Every request follows this routing pattern.

---

# Authentication Flow

```text
Visitor

↓

Login Page

↓

Authentication

↓

Session Created

↓

Authenticated User

↓

Protected Pages

↓

Logout

↓

Session Destroyed
```

Protected views use:

* login_required

Future:

* Permissions
* Groups
* Two-Factor Authentication

---

# Purchase Flow

Current

```text
Product Page

↓

Buy Button

↓

Create Order

↓

Ownership Granted

↓

Dashboard

↓

Download Allowed
```

Future

```text
Cart

↓

Checkout

↓

Stripe

↓

Payment Verification

↓

Order Creation

↓

License Generation

↓

Download Access
```

---

# Download Flow

```text
User

↓

Request Download

↓

Authentication Check

↓

Ownership Check

↓

Locate File

↓

Stream File

↓

Browser Download
```

Files should never be exposed directly.

Downloads must always pass through permission checks.

---

# Database Architecture

Current Models

User

Category

Product

ProductImage

Order

Relationships

User

↓

Order

↓

Product

↓

Category

Product

↓

ProductImage

Future models:

Cart

CartItem

Review

Wishlist

Coupon

License

DownloadHistory

Notification

---

# URL Architecture

```text
/

Homepage

/products/

/products/<slug>/

/products/<slug>/download/

/accounts/login/

/accounts/register/

/accounts/logout/

/accounts/dashboard/

/orders/buy/<slug>/
```

The project uses modular URL routing.

Each app manages its own routes.

---

# File Storage

Current

```text
media/

products/

thumbnails/

product_gallery/
```

Future

Cloud storage may replace local media.

Possible providers:

* Amazon S3
* Cloudflare R2
* Azure Blob Storage

---

# Security Architecture

Current

* Authentication
* Ownership verification
* Protected download views
* Active product validation

Future

* Stripe verification
* Signed download URLs
* Download limits
* Audit logs
* Role-based permissions
* Two-factor authentication

---

# Design Principles

The project follows these principles:

* Modularity
* Single Responsibility Principle
* Separation of Concerns
* DRY (Don't Repeat Yourself)
* KISS (Keep It Simple)
* Maintainability
* Scalability
* Security by Default

---

# Future Refactoring

As complexity increases, business logic should gradually move into:

* Services
* Forms
* Managers
* Utilities
* Validators

Views should become thin controllers that coordinate requests rather than contain complex business logic.

---

# Future Architecture Roadmap

Current

```text
Views

↓

Models

↓

Database
```

Target

```text
Views

↓

Forms

↓

Services

↓

Managers

↓

Models

↓

Database
```

This progression improves maintainability, testability, and separation of responsibilities.

---

# Deployment Vision

Production architecture will eventually include:

```text
Internet

↓

Nginx

↓

Gunicorn

↓

Django

↓

PostgreSQL

↓

Redis

↓

Cloud Storage

↓

Monitoring

↓

Backups
```

---

# Architecture Principles

Every architectural decision should satisfy the following goals:

* Easy to understand
* Easy to extend
* Easy to maintain
* Secure by default
* Well documented
* Suitable for long-term growth

When trade-offs exist, long-term maintainability takes precedence over short-term convenience.

---

# End of Document

This document should evolve as the architecture evolves.

Any significant architectural change must be reflected here before implementation is considered complete.
