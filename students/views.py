from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Avg

from students.models import StudentProfile, StudentSkill
from careers.models import Career, Skill, CareerSkill
from assessments.models import AssessmentSession, AssessmentCategory
from recommendations.models import CareerRecommendationLog
from skill_gap.services import calculate_skill_gap
from roadmap.services import get_student_roadmap_data
from resume_analyzer.models import Resume
from interviews.models import InterviewSession
from projects.models import ProjectIdea

@login_required
def dashboard_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    target_career = profile.target_career or Career.objects.first()
    
    # 1. Career recommendations
    recs = CareerRecommendationLog.objects.filter(student=profile)[:4]
    
    # 2. Skill Gap calculations
    gap_data = calculate_skill_gap(profile, target_career) if target_career else None
    
    # 3. Roadmap progress
    roadmap_data = get_student_roadmap_data(profile, target_career) if target_career else None
    
    # 4. Assessment statuses
    categories = AssessmentCategory.objects.all()
    completed_sessions = AssessmentSession.objects.filter(student=profile, completed=True)
    completed_cat_ids = set(completed_sessions.values_list("category_id", flat=True))
    
    assessment_stats = []
    total_score = 0.0
    for cat in categories:
        sess = completed_sessions.filter(category=cat).first()
        is_done = cat.id in completed_cat_ids
        pct = sess.percentage if sess else 0.0
        if is_done:
            total_score += pct
        assessment_stats.append({
            "category": cat,
            "completed": is_done,
            "score": pct,
            "session": sess
        })
    avg_assessment_score = round(total_score / len(categories), 1) if categories.exists() else 0.0
    
    # 5. Latest Resume
    latest_resume = Resume.objects.filter(student=profile).first()
    
    # 6. Latest Interview Session
    latest_interview = InterviewSession.objects.filter(student=profile, completed=True).first()
    
    # 7. Recommended Projects
    projects = ProjectIdea.objects.filter(career=target_career)[:3] if target_career else ProjectIdea.objects.all()[:3]
    
    context = {
        "profile": profile,
        "target_career": target_career,
        "recommendations": recs,
        "gap_data": gap_data,
        "roadmap_data": roadmap_data,
        "assessment_stats": assessment_stats,
        "avg_assessment_score": avg_assessment_score,
        "latest_resume": latest_resume,
        "latest_interview": latest_interview,
        "projects": projects,
    }
    return render(request, "students/dashboard.html", context)


@login_required
def profile_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    careers = Career.objects.all()
    
    if request.method == "POST":
        profile.phone = request.POST.get("phone", "").strip()
        profile.college = request.POST.get("college", "").strip()
        profile.degree = request.POST.get("degree", "").strip()
        profile.branch = request.POST.get("branch", "").strip()
        profile.graduation_year = int(request.POST.get("graduation_year", 2026))
        profile.cgpa = float(request.POST.get("cgpa", 8.0))
        profile.preferred_work_style = request.POST.get("preferred_work_style", "Technical")
        profile.certifications_count = int(request.POST.get("certifications_count", 0))
        profile.projects_count = int(request.POST.get("projects_count", 0))
        profile.internship_done = request.POST.get("internship_done") == "on"
        profile.bio = request.POST.get("bio", "").strip()
        profile.linkedin_url = request.POST.get("linkedin_url", "").strip()
        profile.github_url = request.POST.get("github_url", "").strip()
        
        target_career_id = request.POST.get("target_career")
        if target_career_id:
            profile.target_career = Career.objects.get(id=target_career_id)
            
        request.user.first_name = request.POST.get("first_name", "").strip()
        request.user.last_name = request.POST.get("last_name", "").strip()
        request.user.save()
        profile.save()
        
        messages.success(request, "Your profile has been updated successfully!")
        return redirect("students:profile")
        
    context = {
        "profile": profile,
        "careers": careers,
    }
    return render(request, "students/profile.html", context)


@login_required
def skills_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    all_skills = Skill.objects.all().order_by("category", "name")
    
    # Existing student ratings
    student_skills_qs = StudentSkill.objects.filter(student=profile)
    student_skill_map = {ss.skill_id: ss.proficiency_level for ss in student_skills_qs}
    
    if request.method == "POST":
        for skill in all_skills:
            field_name = f"skill_{skill.id}"
            if field_name in request.POST:
                val = float(request.POST.get(field_name, 0.0))
                StudentSkill.objects.update_or_create(
                    student=profile,
                    skill=skill,
                    defaults={"proficiency_level": val}
                )
        messages.success(request, "Technical skill ratings successfully saved!")
        return redirect("students:dashboard")
        
    skills_by_category = {}
    for skill in all_skills:
        cat = skill.get_category_display()
        if cat not in skills_by_category:
            skills_by_category[cat] = []
        skills_by_category[cat].append({
            "skill": skill,
            "current_level": student_skill_map.get(skill.id, 5.0)
        })
        
    context = {
        "profile": profile,
        "skills_by_category": skills_by_category,
        "total_skills": all_skills.count(),
    }
    return render(request, "students/skills.html", context)
