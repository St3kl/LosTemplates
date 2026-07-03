from django.contrib import admin

from .models import UserProductAccess


@admin.register(UserProductAccess)
class UserProductAccessAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "product",
        "granted_at",
    )

    search_fields = (
        "user__username",
        "product__title",
    )

    list_filter = (
        "granted_at",
    )