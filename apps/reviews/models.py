
from django.db import models
from django.contrib.auth.models import User

from apps.products.models import Product


class Review(models.Model):

    RATING_CHOICES = [

        (1, "1"),

        (2, "2"),

        (3, "3"),

        (4, "4"),

        (5, "5"),

    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
    )

    comment = models.TextField()

    approved = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        unique_together = (
            "product",
            "user",
        )

        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return f"{self.product} - {self.rating}"