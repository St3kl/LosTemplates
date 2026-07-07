Phase 5.1

Review System

Features

✔ One review per customer

✔ Rating (1-5)

✔ Written comment

✔ Admin moderation

✔ Timestamp

✔ Product relationship

✔ User relationship



STEP 5 — Review Form

Files Created

apps/reviews/forms.py
apps/reviews/services.py

Purpose

• Validate review submissions.
• Separate business logic from views.
• Prepare for verified purchase enforcement.



STEP 6 — Verified Purchase Reviews

Files Created

apps/reviews/views.py
apps/reviews/urls.py

Files Updated

apps/reviews/services.py
config/urls.py

Business Rules

• Only authenticated users can review.
• Only paid customers can review.
• One review per product per user.
• Business logic centralized in ReviewService.