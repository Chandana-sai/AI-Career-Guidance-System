from careers.models import Career, CareerSkill, Skill
from students.models import StudentProfile, StudentSkill

def calculate_skill_gap(student_profile, career):
    """
    Compares student skills against career requirements.
    Returns:
    - readiness_percentage
    - strong_skills
    - moderate_skills
    - skill_gaps
    - radar_data
    - priority_recommendations
    """
    career_skills = CareerSkill.objects.filter(career=career).select_related('skill')
    student_skills_qs = StudentSkill.objects.filter(student=student_profile)
    student_skill_map = {ss.skill_id: ss.proficiency_level for ss in student_skills_qs}
    
    strong_skills = []
    moderate_skills = []
    skill_gaps = []
    
    total_weighted_req = 0.0
    total_weighted_achieved = 0.0
    
    radar_labels = []
    radar_student = []
    radar_required = []
    
    for cs in career_skills:
        skill_name = cs.skill.name
        req_level = float(cs.required_level)
        weight = float(cs.weight)
        stu_level = float(student_skill_map.get(cs.skill_id, 0.0))
        
        radar_labels.append(skill_name)
        radar_student.append(stu_level)
        radar_required.append(req_level)
        
        gap = req_level - stu_level
        pct = min(100.0, round((stu_level / (req_level + 1e-6)) * 100.0, 1))
        
        skill_info = {
            'skill_id': cs.skill.id,
            'name': skill_name,
            'category': cs.skill.get_category_display(),
            'required_level': req_level,
            'student_level': stu_level,
            'gap': max(0.0, round(gap, 1)),
            'match_pct': pct,
            'importance': cs.importance
        }
        
        total_weighted_req += req_level * weight
        total_weighted_achieved += min(req_level, stu_level) * weight
        
        if stu_level >= req_level:
            strong_skills.append(skill_info)
        elif stu_level >= (req_level * 0.45):
            moderate_skills.append(skill_info)
        else:
            skill_gaps.append(skill_info)
            
    readiness_pct = 0.0
    if total_weighted_req > 0:
        readiness_pct = round((total_weighted_achieved / total_weighted_req) * 100.0, 1)
        
    skill_gaps.sort(key=lambda x: (x['importance'] != 'Essential', -x['gap']))
    
    priority_recommendations = []
    for g in skill_gaps[:5]:
        priority_recommendations.append(f"Focus on mastering {g['name']} (Current: {g['student_level']}/10, Target: {g['required_level']}/10).")
        
    return {
        'career': career,
        'readiness_percentage': readiness_pct,
        'strong_skills': strong_skills,
        'moderate_skills': moderate_skills,
        'skill_gaps': skill_gaps,
        'total_skills_evaluated': len(career_skills),
        'strong_count': len(strong_skills),
        'moderate_count': len(moderate_skills),
        'gap_count': len(skill_gaps),
        'radar_chart': {
            'labels': radar_labels,
            'student_scores': radar_student,
            'required_scores': radar_required
        },
        'priority_recommendations': priority_recommendations
    }
