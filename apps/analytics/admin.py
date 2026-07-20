from django.contrib import admin

from .models import (
    ProductView,
    ProductSale,
    ProductDownloadMetric,
)


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "user",
        "ip_address",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "product__title",
        "user__username",
    )


@admin.register(ProductSale)
class ProductSaleAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "user",
        "price",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "product__title",
        "user__username",
    )


@admin.register(ProductDownloadMetric)
class ProductDownloadMetricAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "user",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "product__title",
        "user__username",
    )