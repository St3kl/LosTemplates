from django.shortcuts import get_object_or_404, render

from .models import Product, Category


def product_list(request):

    products = Product.objects.filter(active=True)

    categories = Category.objects.all()

    # --- Filtering by category ---
    category_slug = request.GET.get("category")

    if category_slug:
        products = products.filter(category__slug=category_slug)

    # --- Search ---
    search_query = request.GET.get("search")

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
        active=True
    )

    related_products = Product.objects.filter(
        category=product.category,
        active=True
    ).exclude(id=product.id)[:4]

    context = {
        "product": product,
        "related_products": related_products
    }

    return render(request, "products/product_detail.html", context)
# Create your views here.
