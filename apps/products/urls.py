from django.urls import path
from . import views, admin_views

app_name = "products"

urlpatterns = [

    # =========================
    # ADMIN ROUTES (FIRST!)
    # =========================
    path(
        "admin/",
        admin_views.admin_product_list,
        name="admin_product_list",
    ),

    path(
        "admin/create/",
        admin_views.admin_product_create,
        name="admin_product_create",
    ),

    path(
        "admin/<int:product_id>/edit/",
        admin_views.admin_product_edit,
        name="admin_product_edit",
    ),

    path(
        "admin/<int:product_id>/toggle/",
        admin_views.admin_product_toggle,
        name="admin_product_toggle",
    ),

    # =========================
    # PUBLIC ROUTES
    # =========================
    path(
        "",
        views.product_list,
        name="product_list",
    ),

    path(
        "<slug:slug>/",
        views.product_detail,
        name="product_detail",
    ),

    path(
        "<slug:slug>/download/",
        views.download_product,
        name="product_download",
    ),
]