from django.utils import timezone
from roadmap.models import RoadmapTemplate, RoadmapStage, StudentRoadmapProgress
from careers.models import Career

def get_student_roadmap_data(student_profile, career=None):
    """
    Returns roadmap stages with the student's progress and completion statistics.
    """
    target_career = career or student_profile.target_career
    if not target_career:
        target_career = Career.objects.first()
        
    try:
        template = RoadmapTemplate.objects.get(career=target_career)
    except RoadmapTemplate.DoesNotExist:
        template = RoadmapTemplate.objects.create(
            career=target_career,
            title=f"Custom Fast-Track: {target_career.title}",
            description=f"Structured curriculum for {target_career.title}",
            estimated_months=6
        )
        RoadmapStage.objects.create(
            template=template,
            stage_number=1,
            title="Stage 1: Core Fundamentals & Practical Labs",
            description="Master key concepts and build initial projects.",
            estimated_weeks=4
        )
        
    stages = template.stages.all().prefetch_related("skills_covered")
    
    progress_map = {}
    for p in StudentRoadmapProgress.objects.filter(student=student_profile, stage__in=stages):
        progress_map[p.stage_id] = p
        
    stages_data = []
    completed_count = 0
    in_progress_count = 0
    
    for st in stages:
        p_obj = progress_map.get(st.id)
        if not p_obj:
            p_obj = StudentRoadmapProgress.objects.create(
                student=student_profile,
                stage=st,
                status="Not Started"
            )
            progress_map[st.id] = p_obj
            
        if p_obj.status == "Completed":
            completed_count += 1
        elif p_obj.status == "In Progress":
            in_progress_count += 1
            
        stages_data.append({
            "stage": st,
            "status": p_obj.status,
            "progress_id": p_obj.id,
            "notes": p_obj.notes,
            "completed_at": p_obj.completed_at,
            "skills": list(st.skills_covered.values_list("name", flat=True))
        })
        
    total_stages = len(stages)
    completion_percentage = 0.0
    if total_stages > 0:
        completion_percentage = round((completed_count / total_stages) * 100.0, 1)
        
    return {
        "template": template,
        "career": target_career,
        "stages": stages_data,
        "total_stages": total_stages,
        "completed_stages": completed_count,
        "in_progress_stages": in_progress_count,
        "completion_percentage": completion_percentage,
    }

def update_stage_progress(student_profile, stage_id, new_status, notes=""):
    try:
        progress, created = StudentRoadmapProgress.objects.get_or_create(
            student=student_profile,
            stage_id=stage_id,
            defaults={"status": new_status, "notes": notes}
        )
        if not created:
            progress.status = new_status
            if notes:
                progress.notes = notes
        if new_status == "Completed":
            progress.completed_at = timezone.now()
        else:
            progress.completed_at = None
        progress.save()
        return True, progress
    except Exception as e:
        return False, None
