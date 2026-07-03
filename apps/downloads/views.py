from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from apps.products.models import Product
from .models import DownloadLog
from .services import DownloadService
@login_required
def secure_download(request, product_id):
    """
    Secure download endpoint.
    """

    product = get_object_or_404(
        Product,
        id=product_id,
        active=True,
    )

    if not DownloadService.has_access(
        request.user,
        product,
    ):
        raise Http404(
            "You do not own this product."
        )

    # ----------------------------
    # Local Storage
    # ----------------------------

    if product.file_source == "local":

        if not product.download_file:
            raise Http404(
                "Download file missing."
            )

        return FileResponse(
            product.download_file.open("rb"),
            as_attachment=True,
            filename=product.download_file.name.split("/")[-1],
        )

    # ----------------------------
    # External Storage
    # ----------------------------

    if product.file_source == "external":

        if not product.external_url:
            raise Http404(
                "External file unavailable."
            )

        return redirect(product.external_url)

    raise Http404("Invalid file source.")

@staff_member_required
def download_analytics(request):
    """
    Admin dashboard for download insights.
    """

    # Top downloaded products
    top_products = (
        DownloadLog.objects
        .values("product__title")
        .annotate(total=Count("id"))
        .order_by("-total")[:10]
    )

    # Total downloads
    total_downloads = DownloadLog.objects.count()

    # Unique users
    unique_users = (
        DownloadLog.objects.values("user")
        .distinct()
        .count()
    )

    # Recent activity
    recent_downloads = (
        DownloadLog.objects.select_related("user", "product")
        .order_by("-downloaded_at")[:20]
    )

    context = {
        "top_products": top_products,
        "total_downloads": total_downloads,
        "unique_users": unique_users,
        "recent_downloads": recent_downloads,
    }

    return render(request, "downloads/analytics.html", context)