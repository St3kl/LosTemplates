from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.shortcuts import render

from .models import (
    ProductView,
    ProductSale,
    ProductDownloadMetric,
)


@staff_member_required
def analytics_dashboard(request):
    """
    Main analytics dashboard.
    """

    total_views = ProductView.objects.count()

    total_sales = ProductSale.objects.count()

    total_downloads = ProductDownloadMetric.objects.count()

    revenue = (
        ProductSale.objects.aggregate(
            total=Sum("price")
        )["total"]
        or 0
    )

    top_products = (
        ProductSale.objects
        .values("product__title")
        .annotate(total=Count("id"))
        .order_by("-total")[:10]
    )

    context = {

        "total_views": total_views,

        "total_sales": total_sales,

        "total_downloads": total_downloads,

        "revenue": revenue,

        "top_products": top_products,

    }

    return render(
        request,
        "analytics/dashboard.html",
        context,
    )