from django.db import models
from django.contrib.auth.models import User
from careers.models import Career, Skill

class StudentProfile(models.Model):
    WORK_STYLE_CHOICES = [
        ("Technical", "Technical / Deep Coding"),
        ("Analytical", "Analytical / Data-Driven"),
        ("Creative", "Creative / Design-Oriented"),
        ("Managerial", "Managerial / Business-Focused"),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20, blank=True)
    college = models.CharField(max_length=200, default="Engineering College")
    degree = models.CharField(max_length=100, default="B.Tech")
    branch = models.CharField(max_length=100, default="Computer Science & Engineering")
    graduation_year = models.IntegerField(default=2026)
    cgpa = models.FloatField(default=8.0)
    
    preferred_work_style = models.CharField(max_length=50, choices=WORK_STYLE_CHOICES, default="Technical")
    certifications_count = models.IntegerField(default=0)
    projects_count = models.IntegerField(default=0)
    internship_done = models.BooleanField(default=False)
    
    target_career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True, blank=True, related_name="aspiring_students")
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.degree} {self.branch})"
        
    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username


class StudentSkill(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="skills")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="student_ratings")
    proficiency_level = models.FloatField(default=5.0, help_text="Rating from 0.0 to 10.0")
    verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "skill")

    def __str__(self):
        return f"{self.student.user.username} - {self.skill.name}: {self.proficiency_level}/10"
