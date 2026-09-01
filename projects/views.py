from django.shortcuts import render, get_object_or_404
from projects.models import ProjectIdea
from careers.models import Career, Skill
from students.models import StudentProfile
from projects.services import get_recommended_projects

def projects_list_view(request):
    profile = None
    if request.user.is_authenticated:
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        
    selected_career = request.GET.get("career")
    selected_difficulty = request.GET.get("difficulty")
    
    projects_qs = ProjectIdea.objects.all().select_related("career").prefetch_related("skills_required")
    
    if selected_career:
        projects_qs = projects_qs.filter(career__title__iexact=selected_career)
    if selected_difficulty:
        projects_qs = projects_qs.filter(difficulty=selected_difficulty)
        
    recommended_data = get_recommended_projects(profile) if profile else None
    
    context = {
        "profile": profile,
        "projects": projects_qs,
        "recommended": recommended_data["recommended"] if recommended_data else [],
        "careers": Career.objects.all(),
        "difficulties": ProjectIdea.DIFFICULTY_CHOICES,
        "selected_career": selected_career,
        "selected_difficulty": selected_difficulty
    }
    return render(request, "projects/list.html", context)


def project_detail_view(request, project_id):
    project = get_object_or_404(ProjectIdea, id=project_id)
    skills = project.skills_required.all()
    
    context = {
        "project": project,
        "skills": skills
    }
    return render(request, "projects/detail.html", context)
