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

from django.contrib.auth.decorators import login_required
from django.http import Http404, FileResponse

from apps.products.models import Product
from .services import DownloadService


@login_required
def download_product(request, product_id):

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404("Product not found.")

    if not DownloadService.has_access(request.user, product):
        raise Http404("You do not own this product.")

    if not product.download_file:
        raise Http404("Download unavailable.")

    return FileResponse(
        product.download_file.open("rb"),
        as_attachment=True,
        filename=product.download_file.name.split("/")[-1],
    )