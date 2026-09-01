from django.urls import path
from . import views

app_name = "roadmap"

urlpatterns = [
    path("", views.roadmap_view, name="view"),
    path("update/<int:stage_id>/", views.toggle_stage_status_api, name="toggle_stage"),
]
