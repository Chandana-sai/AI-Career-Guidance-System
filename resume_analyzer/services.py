import re
import os
from pypdf import PdfReader
import docx
from careers.models import Skill, Career, CareerSkill

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    if ext == ".pdf":
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            text = f"Error extracting PDF text: {str(e)}"
    elif ext in [".docx", ".doc"]:
        try:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            text = f"Error extracting DOCX text: {str(e)}"
    else:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception as e:
            text = f"Error reading text file: {str(e)}"
            
    return text.strip()

def analyze_resume_content(text, target_career=None):
    """
    Performs NLP and heuristic extraction on resume text.
    """
    # 1. Contact Information
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    email = email_match.group(0) if email_match else ""
    
    phone_match = re.search(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    phone = phone_match.group(0) if phone_match else ""
    
    # 2. Education keywords
    edu_keywords = ["b.tech", "b.e.", "btech", "m.tech", "bca", "mca", "b.sc", "computer science", "information technology", "cgpa", "gpa", "bachelor", "master"]
    edu_found = []
    text_lower = text.lower()
    for kw in edu_keywords:
        if kw in text_lower:
            edu_found.append(kw.upper())
    education_summary = ", ".join(list(set(edu_found))) if edu_found else "Academic details detected in document."
    
    # 3. Section checks
    has_contact = bool(email or phone)
    has_education = len(edu_found) > 0
    has_projects = bool(re.search(r"\b(projects?|portfolio|capstone)\b", text_lower))
    has_experience = bool(re.search(r"\b(experience|internship|work history|employment)\b", text_lower))
    has_certs = bool(re.search(r"\b(certificat(ions?|es?)|courses?|training)\b", text_lower))
    
    # 4. Skill Extraction against database catalog
    all_skills = list(Skill.objects.all().values_list("name", flat=True))
    detected_skills = []
    
    for s_name in all_skills:
        # Regex search for standalone skill keyword (e.g. 'Python', 'React.js', 'SQL')
        pattern = r"(?:^|\W)" + re.escape(s_name.lower()) + r"(?:$|\W)"
        if re.search(pattern, text_lower):
            detected_skills.append(s_name)
            
    # Also check popular skill aliases
    aliases = {
        "Python": ["python3", "py"],
        "JavaScript": ["js", "es6", "vanilla js"],
        "React.js": ["react", "reactjs"],
        "Django": ["django rest framework", "drf"],
        "Docker": ["dockerfile", "containers"],
        "CI/CD & Git": ["git", "github", "gitlab", "ci/cd"],
        "AWS / Azure / GCP": ["aws", "azure", "gcp", "amazon web services", "s3", "ec2"],
        "SQL": ["mysql", "postgresql", "postgres", "sqlite", "queries"],
        "Machine Learning": ["ml", "scikit", "supervised learning", "regression", "classification"],
        "Deep Learning & NLP": ["nlp", "neural networks", "pytorch", "transformers", "bert", "gpt", "cnn", "lstm"]
    }
    for s_name, syns in aliases.items():
        if s_name not in detected_skills:
            for syn in syns:
                if re.search(r"(?:^|\W)" + re.escape(syn) + r"(?:$|\W)", text_lower):
                    detected_skills.append(s_name)
                    break
                    
    detected_skills = sorted(list(set(detected_skills)))
    
    # 5. Career Skill Match
    missing_skills = []
    relevant_skills = []
    match_percentage = 0.0
    
    if target_career:
        req_skills = list(CareerSkill.objects.filter(career=target_career).values_list("skill__name", flat=True))
        for rs in req_skills:
            if rs in detected_skills:
                relevant_skills.append(rs)
            else:
                missing_skills.append(rs)
                
        if req_skills:
            match_percentage = round((len(relevant_skills) / len(req_skills)) * 100.0, 1)
    else:
        relevant_skills = detected_skills
        
    # 6. Completeness Score
    completeness = 20.0  # baseline
    if has_contact: completeness += 20.0
    if has_education: completeness += 15.0
    if len(detected_skills) >= 4: completeness += 20.0
    elif len(detected_skills) >= 1: completeness += 10.0
    if has_projects: completeness += 15.0
    if has_experience or has_certs: completeness += 10.0
    completeness_score = min(100.0, completeness)
    
    # 7. Constructive feedback
    suggestions = []
    if not email or not phone:
        suggestions.append("Ensure your full email address and contact phone number are clearly visible at the top.")
    if len(detected_skills) < 5:
        suggestions.append("Add a dedicated 'Technical Skills' section categorizing Languages, Frameworks, and Tools.")
    if not has_projects:
        suggestions.append("Include 2-3 substantial technical projects with measurable outcomes and GitHub repository links.")
    if missing_skills and target_career:
        missing_str = ", ".join(missing_skills[:4])
        suggestions.append(f"To target **{target_career.title}**, consider learning and highlighting: **{missing_str}**.")
    if completeness_score < 75:
        suggestions.append("Structure your resume into standard sections: Contact, Education, Skills, Projects, and Experience.")
        
    if not suggestions:
        suggestions.append("Great resume structure! Keep your projects updated with active live URLs.")
        
    return {
        "email": email,
        "phone": phone,
        "education": education_summary,
        "detected_skills": detected_skills,
        "missing_skills": missing_skills,
        "relevant_skills": relevant_skills,
        "completeness_score": completeness_score,
        "match_percentage": match_percentage,
        "feedback_notes": " \n".join(suggestions)
    }
