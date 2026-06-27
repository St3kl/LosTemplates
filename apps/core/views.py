from django.shortcuts import render
from apps.products.models import Product


def home(request):

    featured_products = Product.objects.filter(
        active=True,
        featured=True
    ).order_by("-created_at")[:6]

    context = {
        "featured_products": featured_products
    }

    return render(request, "core/home.html", context)
# Create your views here.
