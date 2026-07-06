from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from apps.products.models import Product

from .forms import ReviewForm
from .services import ReviewService


@login_required
def create_review(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug,
        active=True,
    )

    if not ReviewService.can_review(
        request.user,
        product,
    ):

        messages.error(
            request,
            "Only verified buyers can review this product.",
        )

        return redirect(
            "products:product_detail",
            slug=slug,
        )

    if ReviewService.has_review(
        request.user,
        product,
    ):

        messages.warning(
            request,
            "You have already reviewed this product.",
        )

        return redirect(
            "products:product_detail",
            slug=slug,
        )

    form = ReviewForm(request.POST)

    if form.is_valid():

        ReviewService.create_review(
            user=request.user,
            product=product,
            rating=form.cleaned_data["rating"],
            comment=form.cleaned_data["comment"],
        )

        messages.success(
            request,
            "Review submitted successfully.",
        )

    return redirect(
        "products:product_detail",
        slug=slug,
    )