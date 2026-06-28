from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.products.models import Product
from django.contrib import messages


def cart_view(request):

    cart = request.session.get("cart", [])

    products = []

    total = 0

    for product_id in cart:

        product = get_object_or_404(Product, id=product_id)

        products.append(product)

        total += product.price

    context = {
        "products": products,
        "total": total,
    }

    return render(
        request,
        "cart/cart.html",
        context
    )


@require_POST
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("cart", [])

    product_id = str(product.id)

    if product_id in cart:

        messages.warning(
            request,
            f'"{product.title}" is already in your cart.'
        )

    else:

        cart.append(product_id)

        request.session["cart"] = cart

        messages.success(
            request,
            f'"{product.title}" added to your cart.'
        )

    return redirect("cart:cart")

@require_POST
def remove_from_cart(request, product_id):

    cart = request.session.get("cart", [])

    product = get_object_or_404(Product, id=product_id)

    product_id = str(product.id)

    if product_id in cart:

        cart.remove(product_id)

        request.session["cart"] = cart

        messages.success(
            request,
            f'"{product.title}" removed from your cart.'
        )

    return redirect("cart:cart")