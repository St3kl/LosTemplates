from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect

from apps.products.models import Product
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