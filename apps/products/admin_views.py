from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from .models import Product


@staff_member_required
def admin_product_list(request):
    """
    Display all products for administrators.
    """

    products = (
        Product.objects
        .select_related("category")
        .order_by("-created_at")
    )

    return render(
        request,
        "products/admin/product_list.html",
        {
            "products": products,
        },
    )