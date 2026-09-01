from resources.models import LearningResource
from careers.models import CareerSkill
from students.models import StudentSkill

def get_recommended_resources(student_profile, career=None):
    target_career = career or student_profile.target_career
    
    # Get student skills below 7.0 or missing
    student_skills = dict(StudentSkill.objects.filter(student=student_profile).values_list('skill_id', 'proficiency_level'))
    
    if target_career:
        required_skill_ids = list(CareerSkill.objects.filter(career=target_career).values_list('skill_id', flat=True))
        # Prioritize resources matching required skills where student proficiency is low (< 7.0)
        gap_skill_ids = [s_id for s_id in required_skill_ids if student_skills.get(s_id, 0.0) < 7.0]
        
        if gap_skill_ids:
            recommended_qs = LearningResource.objects.filter(skill_id__in=gap_skill_ids).select_related('skill')
        else:
            recommended_qs = LearningResource.objects.filter(skill_id__in=required_skill_ids).select_related('skill')
    else:
        # Generic recommendation based on all skills < 6
        gap_skill_ids = [s_id for s_id, lvl in student_skills.items() if lvl < 6.0]
        recommended_qs = LearningResource.objects.filter(skill_id__in=gap_skill_ids).select_related('skill')
        
    all_resources = LearningResource.objects.all().select_related('skill')
    
    return {
        'recommended': recommended_qs[:12],
        'all_resources': all_resources[:24],
        'target_career': target_career
    }
