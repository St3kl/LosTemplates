from django.urls import path
from . import views
from . import admin_views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("<slug:slug>/", views.product_detail, name="product_detail"),
    path("<slug:slug>/download/", views.download_product, name="product_download"),
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
]