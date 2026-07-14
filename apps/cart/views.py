from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.orders.models import Order, OrderItem
from apps.products.models import Product


@login_required
def cart_view(request):

    order = (
        Order.objects
        .filter(
            user=request.user,
            status="pending",
        )
        .prefetch_related("items__product")
        .first()
    )

    if order:

        cart_items = (
            order.items
            .select_related("product")
            .all()
        )

        subtotal = order.total_price
        discount = order.discount
        final_total = subtotal - discount

    else:

        cart_items = []
        subtotal = 0
        discount = 0
        final_total = 0

    context = {
        "cart_items": cart_items,
        "order": order,
        "subtotal": subtotal,
        "discount": discount,
        "final_total": final_total,
    }

    return render(
        request,
        "cart/cart.html",
        context,
    )


@require_POST
@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
    )

    order = (
        Order.objects
        .filter(
            user=request.user,
            status="pending",
        )
        .first()
    )

    if order is None:

        order = Order.objects.create(
            user=request.user,
            status="pending",
            total_price=0,
        )

    item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={
            "price": product.price,
        },
    )

    if created:

        messages.success(
            request,
            f'"{product.title}" added to your cart.',
        )

    else:

        messages.warning(
            request,
            f'"{product.title}" is already in your cart.',
        )

    order.total_price = sum(
        item.price
        for item in order.items.all()
    )

    order.save()

    return redirect("cart:cart")


@login_required
def remove_from_cart(request, product_id):

    order = (
        Order.objects
        .filter(
            user=request.user,
            status="pending",
        )
        .first()
    )

    if order:

        OrderItem.objects.filter(
            order=order,
            product_id=product_id,
        ).delete()

        order.total_price = sum(
            item.price
            for item in order.items.all()
        )

        order.save()

        if not order.items.exists():
            order.delete()

    return redirect("cart:cart")