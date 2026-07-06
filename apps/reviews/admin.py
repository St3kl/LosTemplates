from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "user",
        "rating",
        "approved",
        "created_at",
    )

    list_filter = (
        "rating",
        "approved",
    )

    search_fields = (
        "product__title",
        "user__username",
    )

    list_editable = (
        "approved",
    )

    ordering = (
        "-created_at",
    )