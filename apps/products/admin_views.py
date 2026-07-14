from django.contrib.admin.views.decorators import staff_member_required
# from django.shortcuts import render, redirect

from .models import Product
from .forms import ProductForm

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
# from .models import Category

from django.core.paginator import Paginator

@staff_member_required
def admin_product_list(request):
    """
    Display all products for administrators.
    """

    products = Product.objects.select_related(
        "category"
    ).order_by("-created_at")

    search = request.GET.get("search")

    if search:
        products = products.filter(
            title__icontains=search
        )

    status = request.GET.get("status")

    if status == "active":
        products = products.filter(active=True)

    elif status == "archived":
        products = products.filter(active=False)

    category = request.GET.get("category")

    if category:
        products = products.filter(
            category__id=category
        )

    paginator = Paginator(products, 10)

    page_number = request.GET.get("page")

    products = paginator.get_page(page_number)

    return render(
        request,
        "products/admin/product_list.html",
        {
            "products": products,
        },
    )


@staff_member_required
def admin_product_create(request):

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "products:admin_product_list"
            )

    else:

        form = ProductForm()

    return render(
        request,
        "products/admin/product_form.html",
        {
            "form": form,
            "title": "Create Product",
        },
    )
    
@staff_member_required
def admin_product_edit(request, product_id):
    """
    Edit an existing product.
    """

    product = get_object_or_404(
        Product,
        id=product_id,
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "products:admin_product_list"
            )

    else:

        form = ProductForm(
            instance=product,
        )

    return render(
        request,
        "products/admin/product_form.html",
        {
            "form": form,
            "title": f"Edit: {product.title}",
            "product": product,
        },
    )
    
    
@staff_member_required
def admin_product_toggle(request, product_id):
    """
    Archive or restore a product.
    """

    product = get_object_or_404(
        Product,
        id=product_id,
    )

    product.active = not product.active
    product.save()

    return redirect(
        "products:admin_product_list"
    )
    
    