from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from apps.products.models import Product
from django.contrib import messages
from apps.orders.models import Order, OrderItem


@login_required
def cart_view(request):

    order = (
        Order.objects
        .filter(
            user=request.user,
            status="pending"
        )
        .prefetch_related("items__product")
        .first()
    )

    context = {
        "order": order,
    }

    return render(
        request,
        "cart/cart.html",
        context
    )


@require_POST
@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    # Get the user's active cart
    order = (
        Order.objects
        .filter(
            user=request.user,
            status="pending"
        )
        .first()
    )

    # Create a cart if none exists
    if order is None:
        order = Order.objects.create(
            user=request.user,
            status="pending",
            total_price=0
        )

    # Prevent duplicate products
    item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={
            "price": product.price
        }
    )

    if created:
        messages.success(
            request,
            f'"{product.title}" added to your cart.'
        )
    else:
        messages.warning(
            request,
            f'"{product.title}" is already in your cart.'
        )

    # Recalculate total
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
            status="pending"
        )
        .first()
    )

    if order:

        OrderItem.objects.filter(
            order=order,
            product_id=product_id
        ).delete()

        # Recalculate total
        total = sum(
            item.price
            for item in order.items.all()
        )

        order.total_price = total
        order.save()

        # Optional: delete empty cart
        if not order.items.exists():
            order.delete()

    return redirect("cart:cart")