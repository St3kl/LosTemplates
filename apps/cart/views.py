from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.products.models import Product
from django.contrib import messages


def cart_view(request):
    cart = request.session.get("cart", {})

    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity

        products.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

        total += subtotal

    context = {
        "products": products,
        "total": total,
    }

    return render(request, "cart/cart.html", context)


@require_POST
def add_to_cart(request, product_id):

    cart = request.session.get("cart", {})

    product = get_object_or_404(Product, id=product_id)

    product_id = str(product.id)

    if product_id in cart:
        cart[product_id] += 1
        messages.success(
            request,
            f'"{product.title}" quantity updated in your cart.'
        )
    else:
        cart[product_id] = 1
        messages.success(
            request,
            f'"{product.title}" added to your cart.'
        )

    request.session["cart"] = cart

    return redirect("cart:cart")