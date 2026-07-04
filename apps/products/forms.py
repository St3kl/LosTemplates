from django import forms

from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            "category",
            "title",
            "slug",
            "short_description",
            "description",
            "price",
            "thumbnail",
            "download_file",
            "file_source",
            "external_url",
            "file_size_mb",
            "version",
            "featured",
            "active",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 6}
            ),
        }