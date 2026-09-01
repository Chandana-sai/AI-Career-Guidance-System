from django.urls import path
from . import views

app_name = "recommendations"

urlpatterns = [
    path("", views.career_recommendations_view, name="list"),
    path("career/<slug:slug>/", views.career_detail_view, name="detail"),
    path("set-target/<int:career_id>/", views.set_target_career_api, name="set_target"),
]
