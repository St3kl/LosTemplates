from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from apps.orders.models import Order

from .forms import CouponApplyForm
from .services import CouponService


@login_required
def apply_coupon(request):

    if request.method != "POST":
        return redirect("cart:cart")

    form = CouponApplyForm(request.POST)

    if not form.is_valid():
        messages.error(
            request,
            "Invalid coupon.",
        )
        return redirect("cart:cart")

    coupon = CouponService.validate(
        form.cleaned_data["code"],
    )

    if not coupon:
        messages.error(
            request,
            "Coupon is invalid or expired.",
        )
        return redirect("cart:cart")

    order = Order.objects.filter(
        user=request.user,
        status="pending",
    ).first()

    if not order:
        messages.error(
            request,
            "No active cart found.",
        )
        return redirect("cart:cart")

    discount = CouponService.calculate_discount(
        coupon,
        order.total_price,
    )

    order.coupon = coupon
    order.discount = discount
    order.save()

    messages.success(
        request,
        f"Coupon '{coupon.code}' applied successfully!",
    )

    return redirect("cart:cart")