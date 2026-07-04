from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from .models import Product
from .forms import ProductForm

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.core.paginator import Paginator

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