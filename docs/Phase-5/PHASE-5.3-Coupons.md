STEP 2 — Coupon Application

Files Created

apps/coupons/forms.py
apps/coupons/views.py
apps/coupons/urls.py

Files Updated

apps/orders/models.py
config/urls.py

Features

• Apply coupon to pending order
• Validate coupon
• Store coupon on order
• Store discount amount
• User feedback via Django messages


STEP 3 — Cart Integration

Features Added

• Coupon input form
• Discount display
• Final price calculation
• Checkout uses discounted total

Updated Files

apps/cart/views.py
apps/orders/views.py
templates/cart/cart.html