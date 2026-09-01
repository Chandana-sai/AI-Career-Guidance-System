from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from resources.models import LearningResource
from careers.models import Skill, Career
from students.models import StudentProfile
from resources.services import get_recommended_resources

def resources_list_view(request):
    profile = None
    if request.user.is_authenticated:
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        
    selected_skill = request.GET.get("skill")
    selected_category = request.GET.get("category")
    selected_level = request.GET.get("level")
    search_query = request.GET.get("q", "").strip()
    
    resources_qs = LearningResource.objects.all().select_related("skill")
    
    if selected_skill:
        resources_qs = resources_qs.filter(skill__name__iexact=selected_skill)
    if selected_category:
        resources_qs = resources_qs.filter(category=selected_category)
    if selected_level:
        resources_qs = resources_qs.filter(level=selected_level)
    if search_query:
        resources_qs = resources_qs.filter(title__icontains=search_query)
        
    recommended_data = get_recommended_resources(profile) if profile else None
    
    context = {
        "profile": profile,
        "resources": resources_qs,
        "recommended": recommended_data["recommended"] if recommended_data else [],
        "skills": Skill.objects.all(),
        "categories": LearningResource.CATEGORY_CHOICES,
        "levels": LearningResource.LEVEL_CHOICES,
        "selected_skill": selected_skill,
        "selected_category": selected_category,
        "selected_level": selected_level,
        "search_query": search_query
    }
    return render(request, "resources/list.html", context)
