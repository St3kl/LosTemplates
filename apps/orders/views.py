from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.products.models import Product
from .models import Order, OrderItem


@login_required
def purchase_product(request, slug):

    product = get_object_or_404(Product, slug=slug, active=True)

    order, created = Order.objects.get_or_create(
        user=request.user,
        status="pending",
        total_price=product.price
    )

    OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={"price": product.price}
    )

    return redirect("product_detail", slug=slug)


@login_required
def checkout(request):

    cart = request.session.get("cart", [])

    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect("cart:cart")

    products = []
    total = 0

    for product_id in cart:
        product = get_object_or_404(Product, id=product_id)
        products.append(product)
        total += product.price

    order = Order.objects.create(
        user=request.user,
        status="pending",
        total_price=0
    )

    for product in products:
        OrderItem.objects.create(
            order=order,
            product=product,
            price=product.price
        )

    order.total_price = total
    order.save()

    request.session["cart"] = []

    messages.success(request, "Order created successfully!")

    return redirect("orders:success")


def order_success(request):
    return render(request, "orders/success.html")