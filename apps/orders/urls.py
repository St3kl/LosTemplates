from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("buy/<slug:slug>/", views.purchase_product, name="purchase_product"),
    path("checkout/", views.checkout, name="checkout"),
    path("success/", views.order_success, name="success"),
    path("<int:order_id>/", views.order_detail, name="detail"),
    path(
        "purchase/<slug:slug>/",
        views.purchase_product,
        name="purchase_product"
    ),
    path("", views.order_list, name="list"),
    path(
    "download/<int:item_id>/",
    views.download_product,
    name="download"
),
    
]