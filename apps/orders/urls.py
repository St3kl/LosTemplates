from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [

    # =========================
    # ORDER LIST
    # =========================
    path(
        "",
        views.order_list,
        name="order_list",
    ),

    # =========================
    # ORDER DETAIL
    # =========================
    path(
        "<int:order_id>/",
        views.order_detail,
        name="order_detail",
    ),

    # =========================
    # PURCHASE PRODUCT
    # =========================
    path(
        "purchase/<slug:slug>/",
        views.purchase_product,
        name="purchase_product",
    ),

    # =========================
    # CHECKOUT
    # =========================
    path(
        "checkout/",
        views.checkout,
        name="checkout",
    ),

    # =========================
    # PAYMENT SUCCESS
    # =========================
    path(
        "success/",
        views.order_success,
        name="order_success",
    ),

    # =========================
    # DOWNLOAD PURCHASED PRODUCT
    # =========================
    path(
        "download/<int:item_id>/",
        views.download_product,
        name="download_product",
    ),
]