import re
from careers.models import Career, Skill, CareerSkill
from students.models import StudentSkill
from skill_gap.services import calculate_skill_gap

def generate_bot_response(user_message, student_profile=None):
    """
    Retrieval and rule-based Career Advisor with student-specific context.
    """
    msg = user_message.lower().strip()
    
    # Context extraction
    target_career = student_profile.target_career if student_profile else None
    target_title = target_career.title if target_career else "Software Developer"
    
    chips = []
    response_text = ""
    
    # 1. Greetings
    if re.search(r"\b(hello|hi|hey|greetings|morning|evening)\b", msg):
        student_name = student_profile.user.first_name if student_profile and student_profile.user.first_name else "there"
        response_text = f"Hello {student_name}! ?? I am your **AI Career Guidance Advisor**.\n\nI can help you with:\n- Career Recommendations & Suitability\n- Skill Gap Analysis\n- Personalized Learning Roadmaps\n- Recommended Projects & Courses\n- Mock Interview Preparation\n\nWhat would you like to explore today?"
        chips = ["What career is suitable for me?", "What skills am I missing?", "Recommend a project", "Mock interview tips"]
        return response_text, chips
        
    # 2. Career Suitability & Prediction
    if re.search(r"\b(suitable|recommend|career for me|what career|predict|best role)\b", msg):
        if student_profile:
            rec_logs = student_profile.recommendation_logs.all()[:3]
            if rec_logs:
                recs_str = "\n".join([f"**{i+1}. {r.career.title}** ({r.suitability_score}% Match)" for i, r in enumerate(rec_logs)])
                response_text = f"Based on our **Machine Learning Prediction Pipeline**, here are your top career paths:\n\n{recs_str}\n\nYour profile indicates strong alignment with **{rec_logs[0].career.title}**!"
            else:
                response_text = f"You haven't completed all assessments yet! Head over to the **Assessments** tab to take the Interest, Aptitude, and Technical assessments, and our ML model will compute your real-time career suitability score."
        else:
            response_text = "To get a personalized prediction, log in and complete your Academic Profile and Skill Ratings. Our ML model evaluates 20+ dimensions including CGPA, programming skills, and aptitudes."
        chips = ["Take Career Assessment", "Check Skill Gap", "Explore Roadmaps"]
        return response_text, chips

    # 3. Skill Gaps & Missing Skills
    if re.search(r"\b(skill gap|missing skill|what skills|what do i need|skills required)\b", msg):
        # Check if specific career was mentioned
        careers = Career.objects.all()
        matched_career = None
        for c in careers:
            if c.title.lower() in msg:
                matched_career = c
                break
                
        active_career = matched_career or target_career or Career.objects.first()
        
        if student_profile and active_career:
            gap_data = calculate_skill_gap(student_profile, active_career)
            missing = [g['name'] for g in gap_data['skill_gaps']]
            strong = [s['name'] for s in gap_data['strong_skills']]
            
            missing_str = ", ".join(missing[:4]) if missing else "None (You meet all essential requirements!)"
            strong_str = ", ".join(strong[:4]) if strong else "Keep building your initial ratings"
            
            response_text = f"?? **Skill Gap Summary for {active_career.title}** (Readiness: {gap_data['readiness_percentage']}%):\n\n" \
                            f"- **Strong Competencies**: {strong_str}\n" \
                            f"- **High-Priority Gaps**: {missing_str}\n\n" \
                            f"We recommend prioritizing your missing skills in our **Personalized Learning Roadmap**."
        else:
            req_skills = CareerSkill.objects.filter(career=active_career).values_list("skill__name", flat=True)
            skills_str = ", ".join(req_skills)
            response_text = f"For **{active_career.title}**, the essential industry skills include: **{skills_str}**."
            
        chips = [f"Roadmap for {active_career.title}", "Recommended Courses", "Resume Check"]
        return response_text, chips

    # 4. Roadmap & Next Steps
    if re.search(r"\b(roadmap|what should i learn|next step|after python|how to become)\b", msg):
        active_career = target_career or Career.objects.first()
        response_text = f"?? **Recommended Progression for {active_career.title}**:\n\n" \
                        f"1. **Stage 1: Core Fundamentals** (Data structures, Clean Code, Git)\n" \
                        f"2. **Stage 2: Domain Deep-Dive** (Frameworks, Databases, API Architecture)\n" \
                        f"3. **Stage 3: Practical Projects** (Full-scale apps with testing)\n" \
                        f"4. **Stage 4: Deployment & Cloud** (Docker, CI/CD pipelines)\n" \
                        f"5. **Stage 5: Interview Prep** (Mock technical & system design rounds)\n\n" \
                        f"You can track your interactive milestone progress on your **Learning Roadmap** dashboard."
        chips = ["View Full Roadmap", "Recommended Projects", "Practice Interviews"]
        return response_text, chips

    # 5. Project Recommendations
    if re.search(r"\b(project|projects|what to build|portfolio|capstone)\b", msg):
        active_career = target_career or Career.objects.first()
        response_text = f"?? **Top Portfolio Project Ideas for {active_career.title}**:\n\n" \
                        f"- **Intermediate**: Real-Time E-Commerce Analytics Dashboard (SQL, Pandas, BI)\n" \
                        f"- **Advanced**: AI Deep Learning Classifier with Dockerized FastAPI deployment\n" \
                        f"- **Full-Stack**: Microservices Cloud Application with CI/CD and Auth\n\n" \
                        f"Check out the **Projects** tab for step-by-step specifications and deliverables."
        chips = ["Explore Projects Tab", "View Courses", "Upload Resume"]
        return response_text, chips

    # 6. Mock Interview Advice
    if re.search(r"\b(interview|mock interview|prepare|questions|tips)\b", msg):
        response_text = f"?? **Mock Interview Tips for Technical Candidates**:\n\n" \
                        f"1. **Structure with STAR**: For behavioral questions, structure responses into Situation, Task, Action, and Result.\n" \
                        f"2. **State Complexity**: Always mention Big-O Time & Space complexity for algorithms.\n" \
                        f"3. **Explain Trade-offs**: Discuss why you picked SQL vs NoSQL, or Bagging vs Boosting.\n" \
                        f"4. **Practice NLP Evaluation**: Take our interactive **Mock Interview** test to get automated NLP semantic scoring on your answers!"
        chips = ["Start Mock Interview", "Check Skills", "Resume Analyzer"]
        return response_text, chips

    # 7. Fallback / Default
    response_text = f"That's a great question regarding **{user_message}**! As an AI career counselor, I recommend evaluating your current skill proficiencies, reviewing your target career requirements, and testing your knowledge in our Mock Interview module. What specific aspect of your career preparation would you like help with?"
    chips = ["Career Suitability", "Check Skill Gaps", "Learning Roadmap", "Recommended Projects"]
    return response_text, chips
