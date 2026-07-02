from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from apps.orders.models import Order
from apps.products.models import Product


def secure_download(request, product_slug):

    product = get_object_or_404(Product, slug=product_slug)

    order = Order.objects.filter(
        user=request.user,
        items__product=product,
        status="paid"
    ).first()

    if not order:
        return HttpResponseForbidden("Payment required")

    # External file
    if product.file_source == "external":
        return redirect(product.external_url)

    # Local file
    if product.download_file:
        return redirect(product.download_file.url)

    return HttpResponseForbidden("File not available")