from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count, Avg

from students.models import StudentProfile
from careers.models import Career, Skill, CareerSkill
from assessments.models import AssessmentSession, Question
from resources.models import LearningResource
from projects.models import ProjectIdea
from resume_analyzer.models import Resume
from interviews.models import InterviewSession
from ml_models.model_service import CareerModelService

@staff_member_required
def admin_dashboard_view(request):
    total_students = StudentProfile.objects.count()
    total_assessments = AssessmentSession.objects.filter(completed=True).count()
    total_resumes = Resume.objects.count()
    total_interviews = InterviewSession.objects.filter(completed=True).count()
    
    avg_cgpa = StudentProfile.objects.aggregate(Avg("cgpa"))["cgpa__avg"] or 0.0
    
    students = StudentProfile.objects.select_related("user", "target_career").all().order_by("-created_at")[:15]
    careers = Career.objects.annotate(student_count=Count("aspiring_students"))
    
    # ML Model Metadata
    service = CareerModelService()
    ml_metrics = service.get_metrics()
    
    context = {
        "total_students": total_students,
        "total_assessments": total_assessments,
        "total_resumes": total_resumes,
        "total_interviews": total_interviews,
        "avg_cgpa": round(avg_cgpa, 2),
        "students": students,
        "careers": careers,
        "ml_metrics": ml_metrics,
        "total_skills": Skill.objects.count(),
        "total_questions": Question.objects.count(),
        "total_resources": LearningResource.objects.count(),
        "total_projects": ProjectIdea.objects.count(),
    }
    return render(request, "custom_admin/dashboard.html", context)


@staff_member_required
def manage_careers_view(request):
    careers = Career.objects.all()
    
    if request.method == "POST":
        title = request.POST.get("title")
        category = request.POST.get("category", "Software Engineering")
        desc = request.POST.get("description")
        salary = request.POST.get("average_salary", "?8 - ?18 LPA")
        demand = request.POST.get("market_demand", "High")
        
        if title and desc:
            Career.objects.create(
                title=title,
                category=category,
                description=desc,
                average_salary=salary,
                market_demand=demand
            )
            messages.success(request, f"Career '{title}' successfully added!")
            return redirect("custom_admin:manage_careers")
            
    return render(request, "custom_admin/manage_careers.html", {"careers": careers})


@staff_member_required
def manage_questions_view(request):
    questions = Question.objects.all().select_related("category")
    return render(request, "custom_admin/manage_questions.html", {"questions": questions})


@staff_member_required
def manage_resources_view(request):
    resources = LearningResource.objects.all().select_related("skill")
    return render(request, "custom_admin/manage_resources.html", {"resources": resources})
