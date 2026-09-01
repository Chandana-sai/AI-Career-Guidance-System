from django.urls import path
from . import views

app_name = "assessments"

urlpatterns = [
    path("", views.assessment_list_view, name="list"),
    path("take/<str:category_code>/", views.take_assessment_view, name="take"),
    path("result/<int:session_id>/", views.assessment_result_view, name="result"),
]
