from decimal import Decimal

from django.db import models
from django.utils import timezone


class Coupon(models.Model):

    DISCOUNT_TYPES = [
        ("percentage", "Percentage"),
        ("fixed", "Fixed Amount"),
    ]

    code = models.CharField(
        max_length=50,
        unique=True,
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPES,
    )

    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    active = models.BooleanField(
        default=True,
    )

    usage_limit = models.PositiveIntegerField(
        default=1,
    )

    times_used = models.PositiveIntegerField(
        default=0,
    )

    valid_from = models.DateTimeField()

    valid_until = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.code

    @property
    def is_available(self):
        """
            Returns True if the coupon
            can currently be used.
        """

        now = timezone.now()

        return (
            self.active
        and self.times_used < self.usage_limit
        and self.valid_from <= now <= self.valid_until
    )
    