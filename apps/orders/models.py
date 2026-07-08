from django.db import models
from django.conf import settings
from apps.products.models import Product
from apps.coupons.models import Coupon


class Order(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    coupon = models.ForeignKey(
    Coupon,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="orders",
    )

    discount = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0,
    )

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
    
    @property
    def final_price(self):

        return max(
        self.total_price - self.discount,
        0
        )
    
    



class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    downloaded = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.product.title} ({self.order.id})"
# Create your models here.
