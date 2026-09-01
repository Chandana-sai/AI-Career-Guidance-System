from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from assessments.models import AssessmentCategory, Question, AssessmentSession, AssessmentResponse
from students.models import StudentProfile

@login_required
def assessment_list_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    categories = AssessmentCategory.objects.all()
    sessions = AssessmentSession.objects.filter(student=profile)
    session_map = {s.category_id: s for s in sessions}
    
    categories_data = []
    for cat in categories:
        s = session_map.get(cat.id)
        categories_data.append({
            "category": cat,
            "session": s,
            "is_completed": bool(s and s.completed),
            "score": s.percentage if s else 0.0,
            "total_questions": cat.questions.count()
        })
        
    context = {
        "categories_data": categories_data,
        "completed_count": sum(1 for c in categories_data if c["is_completed"]),
        "total_categories": len(categories_data)
    }
    return render(request, "assessments/assessment_list.html", context)


@login_required
def take_assessment_view(request, category_code):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    category = get_object_or_404(AssessmentCategory, code=category_code)
    questions = category.questions.all()
    
    if not questions.exists():
        messages.warning(request, "No questions currently available in this category.")
        return redirect("assessments:list")
        
    if request.method == "POST":
        session, _ = AssessmentSession.objects.get_or_create(
            student=profile,
            category=category,
            defaults={"total_marks": sum(q.marks for q in questions)}
        )
        session.responses.all().delete()
        
        total_awarded = 0.0
        total_possible = 0.0
        
        for q in questions:
            field_name = f"question_{q.id}"
            selected = request.POST.get(field_name, "").strip()
            is_correct = (selected.upper() == q.correct_option.upper())
            marks = float(q.marks) if is_correct else 0.0
            
            total_possible += float(q.marks)
            total_awarded += marks
            
            AssessmentResponse.objects.create(
                session=session,
                question=q,
                selected_option=selected,
                is_correct=is_correct,
                marks_awarded=marks
            )
            
        pct = round((total_awarded / (total_possible + 1e-6)) * 100.0, 1)
        session.score = total_awarded
        session.total_marks = total_possible
        session.percentage = pct
        session.completed = True
        session.completed_at = timezone.now()
        session.save()
        
        messages.success(request, f"You completed the {category.name} assessment with a score of {pct}%!")
        return redirect("assessments:result", session_id=session.id)
        
    context = {
        "category": category,
        "questions": questions,
        "total_questions": questions.count(),
        "time_limit": category.time_limit_minutes
    }
    return render(request, "assessments/take_assessment.html", context)


@login_required
def assessment_result_view(request, session_id):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    session = get_object_or_404(AssessmentSession, id=session_id, student=profile)
    responses = session.responses.all().select_related("question")
    
    context = {
        "session": session,
        "category": session.category,
        "responses": responses,
        "correct_count": responses.filter(is_correct=True).count(),
        "total_count": responses.count()
    }
    return render(request, "assessments/result.html", context)
