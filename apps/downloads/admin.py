from django.contrib import admin

from .models import (
    UserProductAccess,
    DownloadLog,
)


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


@admin.register(DownloadLog)
class DownloadLogAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "product",
        "downloaded_at",
        "ip_address",
    )

    search_fields = (
        "user__username",
        "product__title",
    )

    list_filter = (
        "downloaded_at",
    )