from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from apps.analytics.services import AnalyticsService
from apps.products.models import Product

from .models import DownloadLog
from .security import DownloadSecurity
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

    # -----------------------------
    # Rate Limiting
    # -----------------------------

    if not DownloadSecurity.can_download(request.user):
        return HttpResponse(
            "Please wait a few seconds before downloading again.",
            status=429,
        )

    # -----------------------------
    # File Exists?
    # -----------------------------

    if not product.download_file:
        raise Http404(
            "Download file missing."
        )

    # -----------------------------
    # Log Download
    # -----------------------------

    DownloadLog.objects.create(
        user=request.user,
        product=product,
        ip_address=get_client_ip(request),
        user_agent=request.META.get(
            "HTTP_USER_AGENT",
            "",
        ),
    )

    # -----------------------------
    # Analytics
    # -----------------------------

    AnalyticsService.track_download(
        product=product,
        user=request.user,
    )

    # -----------------------------
    # Download
    # -----------------------------

    return FileResponse(
        product.download_file.open("rb"),
        as_attachment=True,
        filename=product.download_file.name.split("/")[-1],
    )


@staff_member_required
def download_analytics(request):
    """
    Download analytics dashboard.
    """

    top_products = (
        DownloadLog.objects
        .values("product__title")
        .annotate(total=Count("id"))
        .order_by("-total")[:10]
    )

    total_downloads = DownloadLog.objects.count()

    unique_users = (
        DownloadLog.objects
        .values("user")
        .distinct()
        .count()
    )

    recent_downloads = (
        DownloadLog.objects
        .select_related(
            "user",
            "product",
        )
        .order_by("-downloaded_at")[:20]
    )

    return render(
        request,
        "downloads/analytics.html",
        {
            "top_products": top_products,
            "total_downloads": total_downloads,
            "unique_users": unique_users,
            "recent_downloads": recent_downloads,
        },
    )


def get_client_ip(request):

    forwarded = request.META.get(
        "HTTP_X_FORWARDED_FOR"
    )

    if forwarded:
        return forwarded.split(",")[0]

    return request.META.get(
        "REMOTE_ADDR"
    )