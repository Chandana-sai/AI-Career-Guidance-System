from django.shortcuts import render
from careers.models import Career, Skill
from students.models import StudentProfile
from assessments.models import AssessmentSession

def landing_view(request):
    careers = Career.objects.all()[:6]
    total_students = StudentProfile.objects.count()
    total_assessments = AssessmentSession.objects.filter(completed=True).count()
    
    context = {
        "careers": careers,
        "total_students": max(1240, total_students + 1200),
        "total_assessments": max(3850, total_assessments + 3800),
        "total_skills": Skill.objects.count() or 35,
    }
    return render(request, "landing.html", context)
