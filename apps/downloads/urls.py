from django.urls import path
from . import views

app_name = "downloads"

urlpatterns = [
    path(
        "<int:product_id>/",
        views.secure_download,
        name="secure_download",
    ),

    path(
        "analytics/",
        views.download_analytics,
        name="analytics",
    ),
]