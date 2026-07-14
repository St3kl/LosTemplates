from django.shortcuts import get_object_or_404, render, redirect
from apps.orders.models import Order
from .models import Product, Category
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from apps.analytics.services import AnalyticsService
import os
from apps.orders.models import OrderItem
from apps.reviews.services import ReviewService


def product_list(request):

    products = Product.objects.filter(active=True)

    categories = Category.objects.order_by("name")

    # --- Filtering by category ---
    category_slug = request.GET.get("category")

    if category_slug:
        products = products.filter(category__slug=category_slug)

    # --- Search ---
    search_query = request.GET.get("q")

    if search_query:
        products = products.filter(title__icontains=search_query)

    # --- Sorting ---
    sort_by = request.GET.get("sort")

    if sort_by == "price_low":
        products = products.order_by("price")

    elif sort_by == "price_high":
        products = products.order_by("-price")

    else:
        products = products.order_by("-created_at")

    context = {
        "products": products,
        "categories": categories,
        "selected_category": category_slug,
        "search_query": search_query,
        "sort_by": sort_by,
    }

    return render(request, "products/product_list.html", context)


def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug,
        active=True,

    )
    
    AnalyticsService.track_product_view(
    product=product,
    user=request.user if request.user.is_authenticated else None,
    ip_address=request.META.get("REMOTE_ADDR"),
)

    related_products = Product.objects.filter(
        category=product.category,
        active=True
    ).exclude(id=product.id)[:4]

    context = {
    "product": product,
    "related_products": related_products,

    "reviews": ReviewService.product_reviews(product),
    "average_rating": ReviewService.average_rating(product),
    "review_count": ReviewService.total_reviews(product),

    "can_review": (
        request.user.is_authenticated
        and ReviewService.can_review(
            request.user,
            product,
        )
        and not ReviewService.has_review(
            request.user,
            product,
        )
    ),
}
    
    

    return render(request, "products/product_detail.html", context)


@login_required
def download_product(request, slug):

    product = get_object_or_404(Product, slug=slug, active=True)

    # CHECK OWNERSHIP
    has_order = OrderItem.objects.filter(
    order__user=request.user,
    order__status="paid",
    product=product,
).exists()

    if not has_order:
        return redirect(
    "products:product_detail",
    slug=slug,
)

    file_path = product.download_file.path

    if not os.path.exists(file_path):
        raise Http404("File not found")

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename=os.path.basename(file_path)
    )
    
    
    
# Create your views here.
