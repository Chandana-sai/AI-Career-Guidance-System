from django.db import models
from django.utils.text import slugify

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("Programming", "Programming Languages"),
        ("Framework", "Frameworks & Libraries"),
        ("Database", "Database & Storage"),
        ("Cloud_DevOps", "Cloud & DevOps"),
        ("Core_CS", "Core Computer Science & Math"),
        ("Soft_Skills", "Soft Skills & Aptitude"),
        ("Domain", "Domain Specific Knowledge"),
    ]
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Programming")
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Career(models.Model):
    DEMAND_CHOICES = [
        ("Very High", "Very High"),
        ("High", "High"),
        ("Moderate", "Moderate"),
    ]
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    category = models.CharField(max_length=100, default="Software Engineering")
    description = models.TextField()
    responsibilities = models.TextField(help_text="Key day-to-day responsibilities", blank=True)
    average_salary = models.CharField(max_length=100, help_text="e.g. ?8 - ?18 LPA", default="?6 - ?14 LPA")
    market_demand = models.CharField(max_length=50, choices=DEMAND_CHOICES, default="High")
    industry_growth = models.CharField(max_length=50, default="18% Annual Growth")
    icon_class = models.CharField(max_length=50, default="bi-briefcase", help_text="Bootstrap/FontAwesome icon")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CareerSkill(models.Model):
    IMPORTANCE_CHOICES = [
        ("Essential", "Essential"),
        ("Important", "Important"),
        ("Nice to Have", "Nice to Have"),
    ]
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name="required_skills")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="career_requirements")
    required_level = models.FloatField(default=7.0, help_text="Required proficiency from 0 to 10")
    importance = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, default="Essential")
    weight = models.FloatField(default=1.0, help_text="Relative weight in score calculation")

    class Meta:
        unique_together = ("career", "skill")

    def __str__(self):
        return f"{self.career.title} -> {self.skill.name} (Req: {self.required_level}/10)"
