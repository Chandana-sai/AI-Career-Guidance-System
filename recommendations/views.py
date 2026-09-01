from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

from students.models import StudentProfile, StudentSkill
from careers.models import Career, Skill, CareerSkill
from assessments.models import AssessmentSession
from recommendations.models import CareerRecommendationLog
from ml_models.model_service import CareerModelService

@login_required
def career_recommendations_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    
    # Check if student clicked "Recalculate / Predict" or if we fetch existing
    force_recalculate = request.GET.get("recalculate") == "1"
    existing_recs = CareerRecommendationLog.objects.filter(student=profile)
    
    if force_recalculate or not existing_recs.exists():
        # Build student feature dict for ML model
        student_skills = dict(StudentSkill.objects.filter(student=profile).values_list("skill__name", "proficiency_level"))
        
        # Assessment scores
        assessments = {sess.category.code: sess.percentage for sess in AssessmentSession.objects.filter(student=profile, completed=True)}
        
        # Map features
        input_data = {
            "cgpa": profile.cgpa,
            "python": student_skills.get("Python", 5.0),
            "java": student_skills.get("Java", 5.0),
            "cpp": student_skills.get("C++", 5.0),
            "sql": student_skills.get("SQL", 5.0),
            "web_dev": (student_skills.get("HTML5/CSS3", 5.0) + student_skills.get("React.js", 5.0) + student_skills.get("JavaScript", 5.0)) / 3.0,
            "machine_learning": student_skills.get("Machine Learning", 5.0),
            "data_analysis": (student_skills.get("Pandas & NumPy", 5.0) + student_skills.get("Data Visualization", 5.0)) / 2.0,
            "cloud_computing": student_skills.get("AWS / Azure / GCP", 5.0),
            "cybersecurity": student_skills.get("Network Security & Cryptography", 5.0),
            "devops": (student_skills.get("Docker", 5.0) + student_skills.get("CI/CD & Git", 5.0)) / 2.0,
            "ui_ux": (student_skills.get("Figma", 5.0) + student_skills.get("Bootstrap & Tailwind", 5.0)) / 2.0,
            
            # Aptitude & Soft skills from assessments
            "logical_reasoning": assessments.get("aptitude", 65.0) / 10.0,
            "problem_solving": (assessments.get("aptitude", 65.0) + assessments.get("technical", 65.0)) / 20.0,
            "mathematics": assessments.get("aptitude", 65.0) / 10.0,
            "communication": assessments.get("soft_skills", 70.0) / 10.0,
            "teamwork": assessments.get("soft_skills", 70.0) / 10.0,
            
            # Interests from assessment
            "interest_ai": assessments.get("interest", 70.0) / 10.0,
            "interest_web": assessments.get("interest", 65.0) / 10.0,
            "interest_data": assessments.get("interest", 70.0) / 10.0,
            "interest_cybersecurity": assessments.get("interest", 50.0) / 10.0,
            "interest_cloud": assessments.get("interest", 55.0) / 10.0,
            "interest_software_dev": assessments.get("interest", 75.0) / 10.0,
            "interest_ui_ux": assessments.get("interest", 60.0) / 10.0,
            "interest_business": assessments.get("interest", 50.0) / 10.0,
            
            "certifications_count": profile.certifications_count,
            "projects_count": profile.projects_count,
            "internship_done": 1 if profile.internship_done else 0,
            "preferred_work_style": profile.preferred_work_style
        }
        
        # ML Inference
        service = CareerModelService()
        prediction = service.predict(input_data, top_n=5)
        
        # Save to database
        CareerRecommendationLog.objects.filter(student=profile).delete()
        saved_recs = []
        for rank, rec in enumerate(prediction["top_recommendations"], 1):
            c_obj = Career.objects.filter(title=rec["career"]).first()
            if c_obj:
                log_entry = CareerRecommendationLog.objects.create(
                    student=profile,
                    career=c_obj,
                    suitability_score=rec["calibrated_score"],
                    raw_probability=rec["raw_probability"],
                    rank=rank,
                    model_name=prediction["model_used"]
                )
                saved_recs.append(log_entry)
        recommendations = saved_recs
        model_name = prediction["model_used"]
    else:
        recommendations = list(existing_recs.select_related("career"))
        model_name = recommendations[0].model_name if recommendations else "Support Vector Machine"
        
    context = {
        "profile": profile,
        "recommendations": recommendations,
        "model_name": model_name,
        "all_careers": Career.objects.all()
    }
    return render(request, "recommendations/careers.html", context)


@login_required
def set_target_career_api(request, career_id):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    career = get_object_or_404(Career, id=career_id)
    profile.target_career = career
    profile.save()
    messages.success(request, f"Target career successfully set to **{career.title}**! Your skill gaps and roadmap have been updated.")
    return redirect("skill_gap:analysis")


def career_detail_view(request, slug):
    career = get_object_or_404(Career, slug=slug)
    required_skills = career.required_skills.all().select_related("skill")
    projects = career.recommended_projects.all()
    
    context = {
        "career": career,
        "required_skills": required_skills,
        "projects": projects
    }
    return render(request, "recommendations/career_detail.html", context)
