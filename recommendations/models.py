from django.db import models
from students.models import StudentProfile
from careers.models import Career

class CareerRecommendationLog(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="recommendation_logs")
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    suitability_score = models.FloatField(help_text="Calibrated suitability percentage (0-100)")
    raw_probability = models.FloatField(help_text="ML model output probability")
    rank = models.IntegerField(default=1)
    model_name = models.CharField(max_length=100, default="Support Vector Machine")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["rank", "-suitability_score"]

    def __str__(self):
        return f"{self.student.user.username} -> Rank #{self.rank}: {self.career.title} ({self.suitability_score}%)"
