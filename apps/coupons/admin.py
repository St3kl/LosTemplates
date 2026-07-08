from django.contrib import admin

from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "discount_type",
        "value",
        "active",
        "usage_limit",
        "times_used",
        "valid_from",
        "valid_until",
    )

    list_filter = (
        "active",
        "discount_type",
    )

    search_fields = (
        "code",
    )