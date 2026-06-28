from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
import os

from apps.products.models import Product
from .models import Order, OrderItem
from .services import user_can_access_item


# -------------------------
# SINGLE PRODUCT PURCHASE
# -------------------------
@login_required
def purchase_product(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug,
        active=True
    )

    # Get the user's active cart
    order = (
        Order.objects
        .filter(
            user=request.user,
            status="pending"
        )
        .order_by("-created_at")
        .first()
    )

    # Create one if it doesn't exist
    if order is None:
        order = Order.objects.create(
            user=request.user,
            status="pending",
            total_price=0
        )

    # Prevent duplicate products
    OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={
            "price": product.price
        }
    )

    # Update cart total
    total = sum(
        item.price
        for item in order.items.all()
    )

    order.total_price = total
    order.save()

    messages.success(
        request,
        f"{product.title} added to your cart."
    )

    return redirect("cart:cart")


# -------------------------
# CART CHECKOUT
# -------------------------
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

    # Create order
    order = Order.objects.create(
        user=request.user,
        status="pending",
        total_price=0
    )

    # Create items
    for product in products:
        OrderItem.objects.create(
            order=order,
            product=product,
            price=product.price
        )

    # Update total
    order.total_price = total
    order.save()

    # Clear cart
    request.session["cart"] = []

    messages.success(request, "Order created successfully!")

    return redirect("orders:success")


# -------------------------
# SUCCESS PAGE
# -------------------------
def order_success(request):
    return render(request, "orders/success.html")


# -------------------------
# ORDER DETAIL
# -------------------------
@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "orders/detail.html",
        {"order": order}
    )


# -------------------------
# ORDER LIST
# -------------------------
@login_required
def order_list(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "orders/list.html",
        {"orders": orders}
    )


# -------------------------
# SECURE DOWNLOAD SYSTEM
# -------------------------
@login_required
def download_product(request, item_id):

    # Security check (ownership + paid access)
    if not user_can_access_item(request.user, item_id):
        raise Http404("You do not have access to this file.")

    item = get_object_or_404(OrderItem, id=item_id)

    file_path = item.product.download_file.path

    if not os.path.exists(file_path):
        raise Http404("File not found")

    # Mark as downloaded
    item.downloaded = True
    item.save()

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename=os.path.basename(file_path)
    )