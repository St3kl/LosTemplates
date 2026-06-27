from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.products.models import Product
from .models import Order


@login_required
def purchase_product(request, slug):

    product = get_object_or_404(Product, slug=slug, active=True)

    # Prevent duplicate orders
    order, created = Order.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"paid": True}
    )

    return redirect("product_detail", slug=slug)

# Create your views here.
