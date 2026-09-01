from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

from students.models import StudentProfile
from careers.models import Career
from roadmap.services import get_student_roadmap_data, update_stage_progress

@login_required
def roadmap_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    
    career_id = request.GET.get("career_id")
    if career_id:
        target_career = get_object_or_404(Career, id=career_id)
    else:
        target_career = profile.target_career or Career.objects.first()
        
    roadmap_data = get_student_roadmap_data(profile, target_career)
    all_careers = Career.objects.all()
    
    context = {
        "profile": profile,
        "target_career": target_career,
        "roadmap_data": roadmap_data,
        "all_careers": all_careers
    }
    return render(request, "roadmap/view.html", context)


@login_required
def toggle_stage_status_api(request, stage_id):
    if request.method == "POST":
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        new_status = request.POST.get("status", "Completed")
        notes = request.POST.get("notes", "")
        
        success, progress = update_stage_progress(profile, stage_id, new_status, notes)
        if success:
            messages.success(request, f"Stage status updated to **{new_status}**!")
            return redirect("roadmap:view")
            
    return redirect("roadmap:view")
