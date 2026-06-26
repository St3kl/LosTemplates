from django.shortcuts import get_object_or_404, render

from .models import Product


def product_list(request):
    products = Product.objects.filter(active=True)

    context = {
        "products": products,
    }

    return render(request, "products/product_list.html", context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        active=True,
    )

    context = {
        "product": product,
    }

    return render(request, "products/product_detail.html", context)
# Create your views here.
