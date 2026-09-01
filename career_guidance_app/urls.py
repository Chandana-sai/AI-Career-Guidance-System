from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import landing_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing_view, name="landing"),
    path("accounts/", include("accounts.urls")),
    path("students/", include("students.urls")),
    path("assessments/", include("assessments.urls")),
    path("recommendations/", include("recommendations.urls")),
    path("skill-gap/", include("skill_gap.urls")),
    path("roadmap/", include("roadmap.urls")),
    path("resources/", include("resources.urls")),
    path("projects/", include("projects.urls")),
    path("resume-analyzer/", include("resume_analyzer.urls")),
    path("interviews/", include("interviews.urls")),
    path("chatbot/", include("chatbot.urls")),
    path("manage-platform/", include("custom_admin.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
