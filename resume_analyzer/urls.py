from django.urls import path
from . import views

app_name = "resume_analyzer"

urlpatterns = [
    path("", views.resume_upload_view, name="upload"),
    path("report/<int:resume_id>/", views.resume_report_view, name="report"),
]
