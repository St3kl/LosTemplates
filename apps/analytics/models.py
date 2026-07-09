from django.db import models
from django.conf import settings

from apps.products.models import Product


class ProductView(models.Model):
    """
    Tracks product page views.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="views",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    def __str__(self):

        return f"{self.product.title} view"



class ProductSale(models.Model):
    """
    Tracks completed product purchases.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="sales",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    def __str__(self):

        return f"{self.product.title} sale"



class ProductDownloadMetric(models.Model):
    """
    Tracks downloads.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="download_metrics",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    def __str__(self):

        return f"{self.product.title} download"