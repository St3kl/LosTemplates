from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    title = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        unique=True
    )

    short_description = models.CharField(
        max_length=500
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    thumbnail = models.ImageField(
        upload_to="thumbnails/"
    )

    download_file = models.FileField(
    upload_to="products/files/",
    null=True,
    blank=True
)

    file_size_mb = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    version = models.CharField(
        max_length=20,
        default="1.0.0"
    )

    featured = models.BooleanField(
        default=False
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    file_source = models.CharField(
    max_length=20,
    choices=[
        ("local", "Local File"),
        ("external", "External Link"),
    ],
    default="local"
)
    external_url = models.URLField(
    null=True,
    blank=True
)
    
    

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="product_gallery/"
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.product.title} Image"