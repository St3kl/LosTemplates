from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # =========================
    # CORE
    # =========================

    path(
        "",
        include("apps.core.urls"),
    ),


    # =========================
    # PRODUCTS
    # =========================

    path(
        "products/",
        include("apps.products.urls"),
    ),


    # =========================
    # ACCOUNTS
    # =========================

    path(
        "accounts/",
        include("apps.accounts.urls"),
    ),


    # =========================
    # ORDERS
    # =========================

    path(
        "orders/",
        include("apps.orders.urls"),
    ),


    # =========================
    # DJANGO ADMIN
    # =========================

    path(
        "admin/",
        admin.site.urls,
    ),


    # =========================
    # CART
    # =========================

    path(
        "cart/",
        include("apps.cart.urls"),
    ),


    # =========================
    # PAYMENTS
    # =========================

    path(
        "payments/",
        include("apps.payments.urls"),
    ),


    # =========================
    # DOWNLOADS
    # =========================

    path(
        "downloads/",
        include("apps.downloads.urls"),
    ),


    # =========================
    # REVIEWS
    # =========================

    path(
        "reviews/",
        include("apps.reviews.urls"),
    ),


    # =========================
    # WISHLIST
    # =========================

    path(
        "wishlist/",
        include("apps.wishlist.urls"),
    ),


    # =========================
    # COUPONS
    # =========================

    path(
        "coupons/",
        include("apps.coupons.urls"),
    ),


    # =========================
    # ANALYTICS
    # =========================

    path(
        "analytics/",
        include("apps.analytics.urls"),
    ),
    
    path(
    "notifications/",
    include("apps.notifications.urls"),
),

]


# =========================
# DEVELOPMENT MEDIA FILES
# =========================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )