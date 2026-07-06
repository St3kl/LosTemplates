from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [

    path(
        "<slug:slug>/create/",
        views.create_review,
        name="create_review",
    ),

]