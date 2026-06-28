from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("buy/<slug:slug>/", views.purchase_product, name="purchase_product"),
    path("checkout/", views.checkout, name="checkout"),
    path("success/", views.order_success, name="success"),
]