from django.urls import path
from . import views

app_name = "resources"

urlpatterns = [
    path("", views.resources_list_view, name="list"),
]
