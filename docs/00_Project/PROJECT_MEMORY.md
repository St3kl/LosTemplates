# LosTemplates - Project Memory

Document Version: 1.0.0
Project Version: 0.8.0
Status: Active Development
Last Updated: 2026-06-27
Maintainer: Luis Mackus

---

# Purpose

This document serves as the permanent memory of the LosTemplates project.

Unlike traditional documentation, this file records important project decisions, completed milestones, current architecture, future direction, and development assumptions.

Any developer or AI assistant should read this document before contributing to the project.

---

# Project Identity

Project Name:
LosTemplates

Project Type:
Single-Vendor Digital Marketplace

Primary Goal:
Sell downloadable digital products that include their editable source files whenever applicable.

Target Audience:

- Developers
- Designers
- Freelancers
- Small Businesses
- Agencies
- Students
- Content Creators

---

# Core Vision

LosTemplates is designed to become a professional marketplace specializing in downloadable templates and digital resources.

The platform prioritizes:

- Security
- Performance
- Simplicity
- Maintainability
- Scalability
- Professional software engineering practices

The project also functions as a long-term software engineering learning project.

---

# Marketplace Model

Marketplace Type:

Single Vendor

Reason:

The platform owner is the exclusive seller.

This simplifies:

- Licensing
- Product Management
- Payments
- Security
- Administration
- Maintenance

Future Possibility:

Multi-vendor support may be implemented in a future major version, but it is **not** part of the current roadmap.

---

# Product Types

Current target products include:

- Website Templates
- Landing Pages
- Dashboard Templates
- Mobile App Templates
- Desktop App Templates
- HTML Templates
- React Templates
- Django Templates
- Bootstrap Templates
- PowerPoint Templates
- Excel Templates
- Word Templates
- Automation Templates
- Source Code
- UI Kits
- Documentation
- Digital Assets

Every product should include its editable source files whenever applicable.

---

# Current Technology Stack

Backend

- Python
- Django

Frontend

- HTML
- CSS
- Bootstrap
- JavaScript

Database

Development:
SQLite

Production:
PostgreSQL (planned)

Media Storage

Django Media

Version Control

Git
GitHub

---

# Current Architecture

Architecture Style:

Modular Django

Installed Apps

- accounts
- core
- products
- orders

Future Apps

- cart
- checkout
- reviews
- wishlist
- search
- api
- analytics

---

# Completed Phases

✔ Environment Setup

✔ Project Structure

✔ Authentication System

✔ Homepage

✔ Product Catalog

✔ Categories

✔ Product Detail

✔ Product Gallery

✔ Django Administration

✔ Secure Downloads

✔ Purchase Records (Mock)

✔ User Dashboard

✔ Initial Documentation

---

# Current Features

Users can:

- Register
- Login
- Logout
- Browse products
- View product details
- Purchase (mock)
- Download owned products
- View dashboard

Administrator can:

- Create products
- Upload thumbnails
- Upload downloadable files
- Create categories
- Manage galleries

---

# Important Business Rules

Rule 001

Only authenticated users may download products.

---

Rule 002

Products must be active before they can be displayed.

---

Rule 003

Every product belongs to exactly one category.

---

Rule 004

Downloads require ownership.

(Currently simulated using mock purchases.)

---

Rule 005

Products are digital only.

No physical shipping exists.

---

Rule 006

All products should contain source code whenever applicable.

---

# Folder Philosophy

The project follows a modular structure.

Each application is responsible for one business domain.

Example:

accounts

Authentication

products

Catalog

orders

Purchases

core

Homepage

Future applications should follow the same philosophy.

---

# Coding Philosophy

The project emphasizes:

- Readability
- Maintainability
- Reusability
- Simplicity
- Separation of Concerns

Avoid:

- Duplicate code
- Large views
- Hardcoded values
- Tight coupling

---

# Documentation Philosophy

Documentation is treated as part of the software.

Every completed phase should update:

- Project Memory
- Changelog
- Roadmap
- Learning Log

Documentation and code must remain synchronized.

---

# Security Philosophy

Never expose downloadable files directly.

Downloads should always pass through permission checks.

Future security improvements include:

- Stripe verification
- Signed URLs
- License validation
- Download limits
- Audit logs

---

# Known Limitations

Current purchase system is simulated.

Shopping cart is not implemented.

Payments are not implemented.

Search is basic.

No email system exists.

No REST API.

No Docker deployment.

SQLite is still used.

---

# Current Development Focus

Current Phase:

Phase 8

Objective:

Complete professional documentation before expanding the feature set.

---

# Immediate Next Milestones

Phase 8

Complete documentation suite.

Phase 9

Architecture refactoring.

Phase 10

Shopping Cart.

Phase 11

Checkout.

Phase 12

Stripe Integration.

---

# Long-Term Vision

LosTemplates should become:

- Production-ready
- Secure
- Well documented
- Easy to maintain
- Easy to extend

The project should reflect professional software engineering standards rather than tutorial-style code.

---

# AI Collaboration Notes

This project is intentionally developed alongside AI assistance.

The objective is not only to produce working software but also to understand every architectural and implementation decision.

Whenever possible:

- Explain concepts before implementation.
- Prefer clean architecture over shortcuts.
- Document major decisions.
- Keep learning as a primary objective.

---

# End of Document

This document should evolve continuously throughout the life of the project.

It should always represent the current state of LosTemplates.