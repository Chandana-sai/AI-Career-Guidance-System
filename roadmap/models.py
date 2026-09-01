from django.db import models
from careers.models import Career, Skill
from students.models import StudentProfile

class RoadmapTemplate(models.Model):
    career = models.OneToOneField(Career, on_delete=models.CASCADE, related_name="roadmap_template")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    estimated_months = models.IntegerField(default=6)

    def __str__(self):
        return f"Roadmap for {self.career.title}"


class RoadmapStage(models.Model):
    template = models.ForeignKey(RoadmapTemplate, on_delete=models.CASCADE, related_name="stages")
    stage_number = models.IntegerField(default=1)
    title = models.CharField(max_length=150)
    description = models.TextField()
    skills_covered = models.ManyToManyField(Skill, blank=True, related_name="roadmap_stages")
    estimated_weeks = models.IntegerField(default=3)
    learning_outcomes = models.TextField(blank=True, help_text="Bulleted key deliverables")

    class Meta:
        ordering = ["stage_number"]

    def __str__(self):
        return f"{self.template.career.title} - Stage {self.stage_number}: {self.title}"


class StudentRoadmapProgress(models.Model):
    STATUS_CHOICES = [
        ("Not Started", "Not Started"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="roadmap_progress")
    stage = models.ForeignKey(RoadmapStage, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Not Started")
    notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "stage")

    def __str__(self):
        return f"{self.student.user.username} - Stage {self.stage.stage_number}: {self.status}"
