from django.urls import path
from . import views

app_name = "custom_admin"

urlpatterns = [
    path("", views.admin_dashboard_view, name="dashboard"),
    path("careers/", views.manage_careers_view, name="manage_careers"),
    path("questions/", views.manage_questions_view, name="manage_questions"),
    path("resources/", views.manage_resources_view, name="manage_resources"),
]
