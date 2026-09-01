from django.db import models
from careers.models import Career
from students.models import StudentProfile

class InterviewQuestion(models.Model):
    CATEGORY_CHOICES = [
        ("Technical", "Technical / Conceptual"),
        ("HR", "HR / Behavioral"),
        ("System_Design", "Architecture & Design"),
        ("Problem_Solving", "Problem Solving / Scenario"),
    ]
    DIFFICULTY_CHOICES = [
        ("Easy", "Entry / Beginner"),
        ("Medium", "Intermediate"),
        ("Hard", "Advanced"),
    ]
    
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name="interview_questions", null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Technical")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default="Medium")
    question_text = models.TextField()
    reference_answer = models.TextField(help_text="Standard reference answer for NLP semantic matching")
    key_concepts = models.TextField(help_text="Comma-separated mandatory concepts or keywords")
    evaluation_rubric = models.TextField(blank=True, help_text="Specific criteria to look for")

    def get_keywords_list(self):
        return [k.strip().lower() for k in self.key_concepts.split(",") if k.strip()]

    def __str__(self):
        career_name = self.career.title if self.career else "General"
        return f"[{career_name}] [{self.category}] {self.question_text[:60]}..."


class InterviewSession(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="interview_sessions")
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name="interview_attempts")
    difficulty = models.CharField(max_length=20, default="Medium")
    total_questions = models.IntegerField(default=5)
    overall_score = models.FloatField(default=0.0, help_text="Aggregated percentage score")
    feedback_summary = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student.user.username} - {self.career.title} Mock Interview ({self.overall_score:.1f}%)"


class InterviewResponse(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE)
    candidate_answer = models.TextField()
    
    # NLP Metrics
    nlp_score = models.FloatField(default=0.0, help_text="Final weighted question score 0-100")
    similarity_score = models.FloatField(default=0.0, help_text="TF-IDF Cosine similarity 0-100")
    keyword_coverage = models.FloatField(default=0.0, help_text="Percentage of key concepts covered")
    word_count = models.IntegerField(default=0)
    
    matched_keywords = models.JSONField(default=list)
    missing_keywords = models.JSONField(default=list)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"Session #{self.session.id} - Q#{self.question.id} Score: {self.nlp_score:.1f}%"
