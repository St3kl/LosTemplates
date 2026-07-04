from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from .models import Product
from .forms import ProductForm



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