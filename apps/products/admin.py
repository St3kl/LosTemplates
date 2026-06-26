from django.contrib import admin

from .models import (
    Category,
    Product,
    ProductImage
)
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
        "created_at"
    )

    prepopulated_fields = {
        "slug": ("name",)
    }
    
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "category",
        "price",
        "featured",
        "active",
        "created_at"
    )

    list_filter = (
        "category",
        "featured",
        "active"
    )

    search_fields = (
        "title",
        "description"
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    inlines = [
        ProductImageInline
    ]
    
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "display_order"
    )