from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
import os

from apps.analytics.services import AnalyticsService
from apps.products.models import Product

from .models import Order, OrderItem
from .services import user_can_access_item


# ============================================================
# CART HELPERS
# ============================================================

def get_or_create_cart(user):
    """
    Return the user's pending order.

    A pending Order acts as the user's shopping cart.
    """

    order, created = Order.objects.get_or_create(
        user=user,
        status="pending",
        defaults={
            "total_price": 0,
        },
    )

    return order


def recalculate_order_total(order):
    """
    Recalculate the order subtotal from its order items.
    """

    order.total_price = sum(
        item.price
        for item in order.items.all()
    )

    order.save(
        update_fields=[
            "total_price",
            "updated_at",
        ]
    )

    return order


# ============================================================
# SINGLE PRODUCT PURCHASE
# ============================================================

@login_required
def purchase_product(request, slug):
    """
    Add a single product to the user's pending cart.
    """

    product = get_object_or_404(
        Product,
        slug=slug,
        active=True,
    )

    order = get_or_create_cart(
        request.user,
    )

    OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={
            "price": product.price,
        },
    )

    recalculate_order_total(order)

    messages.success(
        request,
        f'"{product.title}" added to your cart.',
    )

    return redirect(
        "products:product_detail",
        slug=product.slug,
    )


# ============================================================
# CART CHECKOUT
# ============================================================

@login_required
def checkout(request):
    """
    Begin checkout for the user's pending order.
    """

    order = (
        Order.objects
        .filter(
            user=request.user,
            status="pending",
        )
        .prefetch_related(
            "items__product",
        )
        .first()
    )

    if not order or not order.items.exists():
        messages.warning(
            request,
            "Your cart is empty.",
        )

        return redirect(
            "cart:cart",
        )

    # The final amount includes any applied coupon discount.
    final_total = order.final_price

    # The final_price property already prevents negative totals.
    if final_total <= 0:
        messages.info(
            request,
            "Your order total is zero. Payment is not required.",
        )

        return redirect(
            "orders:order_success",
        )

    return redirect(
        "payments:start",
        order_id=order.id,
    )


# ============================================================
# ORDER SUCCESS
# ============================================================

def order_success(request):
    """
    Display the order success page.
    """

    return render(
        request,
        "orders/success.html",
    )


# ============================================================
# ORDER DETAIL
# ============================================================

@login_required
def order_detail(request, order_id):
    """
    Display a single order belonging to the current user.
    """

    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items__product",
        ),
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


# ============================================================
# ORDER LIST
# ============================================================

@login_required
def order_list(request):
    """
    Display all orders belonging to the current user.
    """

    orders = (
        Order.objects
        .filter(
            user=request.user,
        )
        .prefetch_related(
            "items__product",
        )
        .order_by(
            "-created_at",
        )
    )

    return render(
        request,
        "orders/list.html",
        {
            "orders": orders,
        },
    )


# ============================================================
# LEGACY SECURE DOWNLOAD
# ============================================================

@login_required
def download_product(request, item_id):
    """
    Download a purchased product.

    Ownership is verified before allowing the download.
    """

    item = get_object_or_404(
        OrderItem.objects.select_related(
            "order",
            "product",
        ),
        id=item_id,
        order__user=request.user,
        order__status="paid",
    )

    product = item.product

    if not product:
        raise Http404(
            "Product not found."
        )

    if not product.download_file:
        raise Http404(
            "Download file is missing."
        )

    if not user_can_access_item(
        request.user,
        item,
    ):
        raise Http404(
            "You do not have access to this product."
        )

    file_path = product.download_file.path

    if not os.path.exists(file_path):
        raise Http404(
            "File not found."
        )

    item.downloaded = True

    item.save(
        update_fields=[
            "downloaded",
        ]
    )

    AnalyticsService.track_download(
        product=product,
        user=request.user,
    )

    return FileResponse(
        product.download_file.open("rb"),
        as_attachment=True,
        filename=os.path.basename(
            product.download_file.name,
        ),
    )
