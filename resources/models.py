from django.db import models
from careers.models import Skill, Career

class LearningResource(models.Model):
    LEVEL_CHOICES = [
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    ]
    CATEGORY_CHOICES = [
        ("Course", "Online Course"),
        ("Tutorial", "Interactive Tutorial"),
        ("Book", "Book / eBook"),
        ("Documentation", "Official Documentation"),
        ("Video", "Video Series"),
        ("Certification", "Certification Path"),
    ]
    
    title = models.CharField(max_length=200)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="resources")
    related_career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True, blank=True, related_name="curated_resources")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Course")
    platform = models.CharField(max_length=100, default="Coursera")
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default="Beginner")
    duration = models.CharField(max_length=50, default="4-6 Weeks")
    description = models.TextField()
    resource_url = models.URLField(max_length=400)
    is_free = models.BooleanField(default=True)
    rating = models.FloatField(default=4.7)

    class Meta:
        ordering = ["-rating", "level"]

    def __str__(self):
        return f"{self.title} ({self.skill.name} - {self.platform})"
