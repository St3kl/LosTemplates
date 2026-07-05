STEP 2 — Notification Model

Files

apps/
└── notifications/
    ├── models.py
    ├── admin.py
    └── apps.py

Purpose

• Store every notification sent by the platform.
• Support read/unread tracking.
• Provide the foundation for an in-app notification center.
• Enable future support for email, push notifications, SMS, and WhatsApp from a unified notification service.

Features

✓ Notification history
✓ Read status
✓ Notification type
✓ User association
✓ Admin management
✓ Automatic ordering

Migration

python manage.py makemigrations notifications
python manage.py migrate