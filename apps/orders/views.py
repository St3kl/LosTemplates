from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
import os

from apps.products.models import Product
from .models import Order, OrderItem
from .services import user_can_access_item


def get_or_create_cart(user):
    """
    Returns the user's pending cart.
    Creates one if it doesn't exist.
    """

    order, created = Order.objects.get_or_create(
        user=user,
        status="pending",
        defaults={"total_price": 0},
    )

    return order


# -------------------------
# SINGLE PRODUCT PURCHASE
# -------------------------

@login_required
def purchase_product(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug,
        active=True,
    )

    order = get_or_create_cart(request.user)

    OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={
            "price": product.price,
        },
    )

    # Always recalculate total
    order.total_price = sum(
        item.price for item in order.items.all()
    )
    order.save()

    return redirect(
        "product_detail",
        slug=slug,
    )


# -------------------------
# CART CHECKOUT
# -------------------------

@login_required
def checkout(request):

    order = (
        Order.objects
        .filter(
            user=request.user,
            status="pending",
        )
        .prefetch_related("items")
        .first()
    )

    if not order or not order.items.exists():

        messages.warning(
            request,
            "Your cart is empty.",
        )

        return redirect("cart:cart")

    # Calculate final price after coupon
    final_total = order.final_price

    # Prevent negative totals
    if final_total < 0:
        final_total = 0

    # No need to save final_price because it's a property

    return redirect(
        "payments:start",
        order_id=order.id,
    )

    # Calculate final price after coupon

    final_total = order.final_price


    # Prevent negative totals

    if final_total < 0:
        final_total = 0


    order.final_price = final_total

    order.save()


    return redirect(
        "payments:start",
        order_id=order.id,
    )


# -------------------------
# SUCCESS PAGE
# -------------------------

def order_success(request):
    return render(
        request,
        "orders/success.html",
    )


# -------------------------
# ORDER DETAIL
# -------------------------

@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    return render(
        request,
        "orders/detail.html",
        {
            "order": order,
        },
    )


# -------------------------
# ORDER LIST
# -------------------------

@login_required
def order_list(request):

    orders = (
        Order.objects
        .filter(user=request.user)
        .order_by("-created_at")
    )

    return render(
        request,
        "orders/list.html",
        {
            "orders": orders,
        },
    )


# -------------------------
# SECURE DOWNLOAD SYSTEM
# -------------------------

@login_required
def download_product(request, item_id):

    item = get_object_or_404(
        OrderItem,
        id=item_id,
    )

    file_path = item.product.download_file.path

    if not os.path.exists(file_path):
        raise Http404("File not found")

    item.downloaded = True
    item.save()

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename=os.path.basename(file_path),
    )