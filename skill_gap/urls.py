from django.urls import path
from . import views

app_name = "skill_gap"

urlpatterns = [
    path("", views.skill_gap_view, name="analysis"),
    path("api/", views.skill_gap_api, name="api"),
]
