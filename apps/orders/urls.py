from django.urls import path
from . import views

urlpatterns = [
    path("buy/<slug:slug>/", views.purchase_product, name="purchase_product"),
]