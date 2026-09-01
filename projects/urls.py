from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path("", views.projects_list_view, name="list"),
    path("<int:project_id>/", views.project_detail_view, name="detail"),
]
