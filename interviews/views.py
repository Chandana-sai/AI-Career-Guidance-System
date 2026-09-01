from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg

from students.models import StudentProfile
from careers.models import Career
from interviews.models import InterviewQuestion, InterviewSession, InterviewResponse
from interviews.services import evaluate_interview_answer

@login_required
def interview_start_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    careers = Career.objects.all()
    past_sessions = InterviewSession.objects.filter(student=profile, completed=True)
    
    if request.method == "POST":
        career_id = request.POST.get("career")
        difficulty = request.POST.get("difficulty", "Medium")
        
        target_career = get_object_or_404(Career, id=career_id) if career_id else (profile.target_career or careers.first())
        
        # Get questions
        qs = InterviewQuestion.objects.filter(career=target_career)
        if not qs.exists():
            qs = InterviewQuestion.objects.filter(career__isnull=True)
        if not qs.exists():
            qs = InterviewQuestion.objects.all()
            
        questions = list(qs[:5])
        
        session = InterviewSession.objects.create(
            student=profile,
            career=target_career,
            difficulty=difficulty,
            total_questions=len(questions)
        )
        return redirect("interviews:room", session_id=session.id)
        
    context = {
        "profile": profile,
        "careers": careers,
        "past_sessions": past_sessions,
        "difficulties": InterviewQuestion.DIFFICULTY_CHOICES
    }
    return render(request, "interviews/mock_interview.html", context)


@login_required
def interview_room_view(request, session_id):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    session = get_object_or_404(InterviewSession, id=session_id, student=profile)
    
    # Pick questions for this session's career
    qs = InterviewQuestion.objects.filter(career=session.career)
    if not qs.exists():
        qs = InterviewQuestion.objects.filter(career__isnull=True)
    if not qs.exists():
        qs = InterviewQuestion.objects.all()
        
    questions = list(qs[:5])
    
    if request.method == "POST":
        total_score = 0.0
        session.responses.all().delete()
        
        for q in questions:
            field_name = f"answer_{q.id}"
            ans_text = request.POST.get(field_name, "").strip()
            
            # Evaluate using NLP
            eval_res = evaluate_interview_answer(q, ans_text)
            
            InterviewResponse.objects.create(
                session=session,
                question=q,
                candidate_answer=ans_text,
                nlp_score=eval_res["nlp_score"],
                similarity_score=eval_res["similarity_score"],
                keyword_coverage=eval_res["keyword_coverage"],
                word_count=eval_res["word_count"],
                matched_keywords=eval_res["matched_keywords"],
                missing_keywords=eval_res["missing_keywords"],
                feedback=eval_res["feedback"]
            )
            total_score += eval_res["nlp_score"]
            
        avg_score = round(total_score / len(questions), 1) if questions else 0.0
        session.overall_score = avg_score
        session.completed = True
        
        # Build summary
        if avg_score >= 80:
            session.feedback_summary = "Outstanding interview performance! You communicated clearly, covered critical keywords, and showed high conceptual mastery."
        elif avg_score >= 60:
            session.feedback_summary = "Solid interview attempt. You showed good baseline knowledge, but practicing more structured explanations will elevate your performance."
        else:
            session.feedback_summary = "Needs more preparation. We recommend revisiting the core roadmap stages and reviewing reference answers."
            
        session.save()
        messages.success(request, f"Mock interview completed! Your overall NLP score is {avg_score}%.")
        return redirect("interviews:result", session_id=session.id)
        
    context = {
        "session": session,
        "career": session.career,
        "questions": questions,
        "total_questions": len(questions)
    }
    return render(request, "interviews/interview_room.html", context)


@login_required
def interview_result_view(request, session_id):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    session = get_object_or_404(InterviewSession, id=session_id, student=profile)
    responses = session.responses.all().select_related("question")
    
    context = {
        "session": session,
        "career": session.career,
        "responses": responses
    }
    return render(request, "interviews/interview_result.html", context)
