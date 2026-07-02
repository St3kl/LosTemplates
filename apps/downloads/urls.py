from django.urls import path
from .views import secure_download

urlpatterns = [
    path("<slug:product_slug>/", secure_download, name="secure_download"),
]