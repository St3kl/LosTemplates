from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

from apps.products.models import Product


class UserProductAccess(models.Model):
    """
    Records permanent ownership of purchased products.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user} owns {self.product}"
    
    
    
User = get_user_model()


class DownloadLog(models.Model):
    """
    Tracks every download event for analytics + security.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="download_logs",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="download_logs",
    )

    ip_address = models.GenericIPAddressField(null=True, blank=True)

    user_agent = models.TextField(blank=True)

    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} → {self.product}"