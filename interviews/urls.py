from django.urls import path
from . import views

app_name = "interviews"

urlpatterns = [
    path("", views.interview_start_view, name="start"),
    path("room/<int:session_id>/", views.interview_room_view, name="room"),
    path("result/<int:session_id>/", views.interview_result_view, name="result"),
]
