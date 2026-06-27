# AI_CONTEXT.md

Document Version: 1.0.0
Project Version: 0.8.0
Purpose: AI Project Context
Last Updated: 2026-06-27

---

# Project Summary

Project Name:
LosTemplates

Type:
Single-Vendor Digital Marketplace

Primary Purpose:
Sell downloadable digital templates and digital resources.

Owner:
Luis Mackus

Current Status:
Active Development

---

# Business Model

Single Vendor Marketplace

Only the project owner sells products.

No vendor management exists.

No marketplace commissions exist.

Future multi-vendor support is outside the current roadmap.

---

# Primary Objectives

Develop a production-quality Django application.

Follow professional software engineering practices.

Keep documentation synchronized with implementation.

Prioritize maintainability over rapid feature development.

Teach software engineering concepts throughout development.

---

# Technology Stack

Backend

Python

Django

Frontend

HTML

CSS

Bootstrap 5

JavaScript

Database

SQLite (Development)

PostgreSQL (Production Planned)

Media

Django Media Storage

Version Control

Git

GitHub

---

# Current Django Apps

accounts

Authentication

core

Homepage

products

Product catalog

orders

Purchase records

---

# Planned Apps

cart

checkout

reviews

wishlist

search

api

analytics

notifications

---

# Current Features

Authentication

Product Catalog

Categories

Product Detail Pages

Product Gallery

Admin Management

Protected Downloads

Purchase Simulation

Dashboard

---

# Completed Phases

Environment

Project Structure

Authentication

Homepage

Catalog

Products

Downloads

Orders

Dashboard

Documentation (In Progress)

---

# Current Phase

Phase 8

Documentation & Project Governance

---

# Documentation Structure

docs/

00_Project

01_Architecture

02_Development

03_UI_UX

04_Security

05_API

06_Deployment

07_AI

assets

---

# Current Folder Structure

LosTemplates/

apps/

config/

templates/

static/

media/

docs/

manage.py

README.md

---

# Coding Standards

Use modular Django apps.

Keep business logic out of templates.

Favor reusable code.

Document every completed phase.

Avoid duplicated logic.

Keep naming consistent.

Use Django best practices.

---

# Architecture Principles

Modular Architecture

Separation of Concerns

Single Responsibility

Documentation First

Security First

Scalability

Maintainability

---

# Database Models

Category

Product

ProductImage

Order

User (Django)

---

# Business Rules

Only authenticated users may download.

Downloads require ownership.

Products must be active.

Every product belongs to one category.

Products are digital only.

Products should include editable source files whenever applicable.

---

# Security Rules

Downloads must pass through Django views.

Never expose downloadable files directly.

Future Stripe verification required.

Future signed download URLs planned.

---

# Current Limitations

No shopping cart.

No payment gateway.

No reviews.

No wishlist.

No API.

No email system.

SQLite only.

No Docker.

---

# Immediate Priorities

Complete documentation.

Improve architecture.

Implement shopping cart.

Implement checkout.

Stripe integration.

License system.

REST API.

---

# Learning Philosophy

Always explain concepts before implementation.

Teach software engineering principles.

Encourage best practices.

Optimize for understanding rather than speed.

---

# AI Instructions

When assisting with this project:

Prefer maintainable solutions.

Explain architectural decisions.

Avoid unnecessary complexity.

Keep documentation updated.

Respect existing project conventions.

Recommend improvements when appropriate.

Always preserve modular architecture.

---

# End of Context