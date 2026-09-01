from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os

from students.models import StudentProfile
from careers.models import Career
from resume_analyzer.models import Resume
from resume_analyzer.services import extract_text_from_file, analyze_resume_content

@login_required
def resume_upload_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    careers = Career.objects.all()
    latest_resume = Resume.objects.filter(student=profile).first()
    
    if request.method == "POST":
        resume_file = request.FILES.get("resume_file")
        career_id = request.POST.get("target_career")
        
        if not resume_file:
            messages.error(request, "Please select a resume file to upload.")
            return render(request, "resume_analyzer/upload.html", {"careers": careers, "latest_resume": latest_resume})
            
        target_career = Career.objects.filter(id=career_id).first() if career_id else profile.target_career
        
        # Save resume model
        resume_obj = Resume.objects.create(
            student=profile,
            target_career=target_career,
            resume_file=resume_file,
            original_filename=resume_file.name
        )
        
        # Extract text
        file_path = resume_obj.resume_file.path
        extracted_text = extract_text_from_file(file_path)
        
        # NLP analysis
        analysis = analyze_resume_content(extracted_text, target_career)
        
        resume_obj.extracted_text = extracted_text
        resume_obj.detected_email = analysis["email"]
        resume_obj.detected_phone = analysis["phone"]
        resume_obj.detected_education = analysis["education"]
        resume_obj.detected_skills = analysis["detected_skills"]
        resume_obj.missing_skills = analysis["missing_skills"]
        resume_obj.relevant_skills = analysis["relevant_skills"]
        resume_obj.completeness_score = analysis["completeness_score"]
        resume_obj.match_percentage = analysis["match_percentage"]
        resume_obj.feedback_notes = analysis["feedback_notes"]
        resume_obj.save()
        
        messages.success(request, f"Resume successfully analyzed with a Completeness Score of {analysis['completeness_score']}%!")
        return redirect("resume_analyzer:report", resume_id=resume_obj.id)
        
    context = {
        "profile": profile,
        "careers": careers,
        "latest_resume": latest_resume
    }
    return render(request, "resume_analyzer/upload.html", context)


@login_required
def resume_report_view(request, resume_id):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    resume = get_object_or_404(Resume, id=resume_id, student=profile)
    
    context = {
        "profile": profile,
        "resume": resume,
        "target_career": resume.target_career or profile.target_career,
        "detected_skills": resume.detected_skills,
        "missing_skills": resume.missing_skills,
        "relevant_skills": resume.relevant_skills,
    }
    return render(request, "resume_analyzer/report.html", context)
