from django.contrib import admin

from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "discount_type",
        "value",
        "active",
        "times_used",
        "usage_limit",
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

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "times_used",
        "created_at",
    )