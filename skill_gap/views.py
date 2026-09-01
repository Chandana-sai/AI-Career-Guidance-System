from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from students.models import StudentProfile
from careers.models import Career
from skill_gap.services import calculate_skill_gap

@login_required
def skill_gap_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    
    career_id = request.GET.get("career_id")
    if career_id:
        target_career = get_object_or_404(Career, id=career_id)
    else:
        target_career = profile.target_career or Career.objects.first()
        
    gap_data = calculate_skill_gap(profile, target_career) if target_career else None
    all_careers = Career.objects.all()
    
    context = {
        "profile": profile,
        "target_career": target_career,
        "gap_data": gap_data,
        "all_careers": all_careers
    }
    return render(request, "skill_gap/analysis.html", context)


@login_required
def skill_gap_api(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    career_id = request.GET.get("career_id")
    if career_id:
        target_career = get_object_or_404(Career, id=career_id)
    else:
        target_career = profile.target_career or Career.objects.first()
        
    gap_data = calculate_skill_gap(profile, target_career)
    return JsonResponse(gap_data)
