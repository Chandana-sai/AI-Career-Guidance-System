from django.db import models
from careers.models import Career, Skill

class ProjectIdea(models.Model):
    DIFFICULTY_CHOICES = [
        ("Beginner", "Beginner (1-2 Weeks)"),
        ("Intermediate", "Intermediate (3-5 Weeks)"),
        ("Advanced", "Advanced / Capstone (6-8 Weeks)"),
    ]
    title = models.CharField(max_length=200)
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name="recommended_projects")
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES, default="Intermediate")
    summary = models.CharField(max_length=300, default="Build a real-world hands-on project.")
    description = models.TextField()
    skills_required = models.ManyToManyField(Skill, related_name="project_ideas")
    key_features = models.TextField(help_text="Key features to build in the project")
    deliverables = models.TextField(help_text="What student will deliver (Repo, Demo, Report)")
    architecture_overview = models.TextField(blank=True)
    estimated_hours = models.IntegerField(default=40)
    github_starter_url = models.URLField(blank=True, default="https://github.com")

    def __str__(self):
        return f"{self.title} [{self.career.title} - {self.difficulty}]"
