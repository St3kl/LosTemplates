from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.shortcuts import render

from apps.orders.models import Order
from apps.payments.models import Payment
from apps.products.models import Product


User = get_user_model()


def home(request):
    featured_products = (
        Product.objects
        .filter(
            active=True,
            featured=True,
        )
        .select_related("category")
        .order_by("-created_at")[:6]
    )

    context = {
        "featured_products": featured_products,
    }

    return render(
        request,
        "core/home.html",
        context,
    )


@staff_member_required
def admin_dashboard(request):
    context = {
        "users": User.objects.count(),
        "products": Product.objects.count(),
        "orders": Order.objects.count(),
        "payments": Payment.objects.count(),
    }

    return render(
        request,
        "core/admin_dashboard.html",
        context,
    )