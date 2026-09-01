from django.db import models
from students.models import StudentProfile
from careers.models import Skill

class AssessmentCategory(models.Model):
    CODE_CHOICES = [
        ("interest", "Career & Domain Interests"),
        ("aptitude", "Logical & Quantitative Aptitude"),
        ("technical", "Core Technical & Programming"),
        ("soft_skills", "Communication & Workplace Skills"),
    ]
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, choices=CODE_CHOICES, unique=True)
    description = models.TextField()
    time_limit_minutes = models.IntegerField(default=15)
    total_questions_to_ask = models.IntegerField(default=10)
    icon_class = models.CharField(max_length=50, default="bi-award")

    def __str__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey(AssessmentCategory, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=10, help_text="A, B, C, D or Likert 1-5")
    explanation = models.TextField(blank=True)
    skill_tag = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name="assessment_questions")
    marks = models.IntegerField(default=1)

    def __str__(self):
        return f"[{self.category.code.upper()}] {self.question_text[:60]}..."


class AssessmentSession(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="assessment_sessions")
    category = models.ForeignKey(AssessmentCategory, on_delete=models.CASCADE, related_name="sessions")
    score = models.FloatField(default=0.0)
    total_marks = models.FloatField(default=0.0)
    percentage = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.category.name}: {self.percentage:.1f}%"


class AssessmentResponse(models.Model):
    session = models.ForeignKey(AssessmentSession, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=10)
    is_correct = models.BooleanField(default=False)
    marks_awarded = models.FloatField(default=0.0)

    def __str__(self):
        return f"Session #{self.session.id} - Q#{self.question.id}: {self.selected_option} ({self.marks_awarded} pts)"
