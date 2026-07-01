from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [

    path(
        "pay/<int:order_id>/",
        views.start_payment,
        name="start",
    ),

    path(
        "callback/",
        views.payment_callback,
        name="callback",
    ),

    path(
        "webhook/",
        views.paystack_webhook,
        name="webhook",
    ),
]