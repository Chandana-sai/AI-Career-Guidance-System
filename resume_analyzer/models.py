from django.db import models
from students.models import StudentProfile
from careers.models import Career

class Resume(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="resumes")
    target_career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True, blank=True)
    resume_file = models.FileField(upload_to="resumes/")
    original_filename = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # NLP Parsed fields
    extracted_text = models.TextField(blank=True)
    candidate_name = models.CharField(max_length=150, blank=True)
    detected_email = models.CharField(max_length=150, blank=True)
    detected_phone = models.CharField(max_length=50, blank=True)
    detected_education = models.TextField(blank=True)
    
    # Skills analysis JSON
    detected_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    relevant_skills = models.JSONField(default=list)
    
    # Scoring
    completeness_score = models.FloatField(default=0.0, help_text="0 to 100 based on structure and sections")
    match_percentage = models.FloatField(default=0.0, help_text="0 to 100 match with target career")
    feedback_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Resume of {self.student.user.username} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"
