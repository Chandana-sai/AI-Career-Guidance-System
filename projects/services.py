from projects.models import ProjectIdea
from careers.models import Career

def get_recommended_projects(student_profile, career=None):
    target_career = career or student_profile.target_career
    
    if target_career:
        projects_qs = ProjectIdea.objects.filter(career=target_career).prefetch_related('skills_required')
    else:
        projects_qs = ProjectIdea.objects.all().prefetch_related('skills_required')
        
    all_projects = ProjectIdea.objects.all().select_related('career').prefetch_related('skills_required')
    
    return {
        'recommended': projects_qs[:6],
        'all_projects': all_projects[:18],
        'target_career': target_career
    }
