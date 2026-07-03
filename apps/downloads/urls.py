from django.urls import path
from .views import secure_download
from . import views

app_name = "downloads"

urlpatterns = [
    path("<slug:product_slug>/", secure_download, name="secure_download"),
    path(
        "<int:product_id>/",
        views.download_product,
        name="download",
    ),
]