from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from apps.products.models import Product

from .services import WishlistService


@login_required
def wishlist(request):
    """
    Display the user's wishlist.
    """

    items = WishlistService.user_items(
        request.user,
    )

    return render(
        request,
        "wishlist/list.html",
        {
            "items": items,
        },
    )


@login_required
def toggle_wishlist(request, product_id):
    """
    Add or remove a product from the wishlist.
    """

    product = get_object_or_404(
        Product,
        id=product_id,
        active=True,
    )

    WishlistService.toggle(
        request.user,
        product,
    )

    return redirect(
        "products:product_detail",
        slug=product.slug,
    )