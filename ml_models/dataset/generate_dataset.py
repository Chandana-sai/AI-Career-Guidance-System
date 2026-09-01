import os
import numpy as np
import pandas as pd

def generate_career_dataset(num_samples=3500, random_state=42):
    np.random.seed(random_state)
    
    careers = [
        "Software Developer",
        "Data Analyst",
        "Data Scientist",
        "Machine Learning Engineer",
        "AI Engineer",
        "Web Developer",
        "Cybersecurity Analyst",
        "Cloud Engineer",
        "DevOps Engineer",
        "UI/UX Developer",
        "Business Analyst"
    ]
    
    # Define archetypes: baseline profile tendencies per career
    archetypes = {
        "Software Developer": {
            "python": 7.5, "java": 8.0, "cpp": 7.5, "sql": 6.5, "web_dev": 6.0,
            "machine_learning": 3.0, "data_analysis": 4.0, "cloud_computing": 5.0,
            "cybersecurity": 4.0, "devops": 5.0, "ui_ux": 4.0,
            "logical_reasoning": 8.0, "problem_solving": 8.5, "mathematics": 7.0,
            "communication": 6.5, "teamwork": 7.0,
            "interest_ai": 4.0, "interest_web": 6.0, "interest_data": 4.0,
            "interest_cybersecurity": 4.0, "interest_cloud": 5.0,
            "interest_software_dev": 9.0, "interest_ui_ux": 4.0, "interest_business": 4.0,
            "pref_style": "Technical"
        },
        "Data Analyst": {
            "python": 7.0, "java": 3.0, "cpp": 2.0, "sql": 8.5, "web_dev": 3.0,
            "machine_learning": 4.5, "data_analysis": 9.0, "cloud_computing": 4.0,
            "cybersecurity": 2.0, "devops": 3.0, "ui_ux": 5.0,
            "logical_reasoning": 8.0, "problem_solving": 7.5, "mathematics": 7.5,
            "communication": 8.0, "teamwork": 7.5,
            "interest_ai": 5.0, "interest_web": 3.0, "interest_data": 9.5,
            "interest_cybersecurity": 2.0, "interest_cloud": 4.0,
            "interest_software_dev": 4.0, "interest_ui_ux": 5.0, "interest_business": 8.0,
            "pref_style": "Analytical"
        },
        "Data Scientist": {
            "python": 8.5, "java": 4.0, "cpp": 4.0, "sql": 8.0, "web_dev": 3.5,
            "machine_learning": 8.5, "data_analysis": 8.5, "cloud_computing": 5.5,
            "cybersecurity": 3.0, "devops": 4.0, "ui_ux": 4.0,
            "logical_reasoning": 8.5, "problem_solving": 8.5, "mathematics": 9.0,
            "communication": 7.5, "teamwork": 7.0,
            "interest_ai": 8.5, "interest_web": 3.0, "interest_data": 9.0,
            "interest_cybersecurity": 3.0, "interest_cloud": 5.0,
            "interest_software_dev": 5.0, "interest_ui_ux": 4.0, "interest_business": 7.0,
            "pref_style": "Analytical"
        },
        "Machine Learning Engineer": {
            "python": 9.0, "java": 5.0, "cpp": 7.0, "sql": 7.0, "web_dev": 4.0,
            "machine_learning": 9.0, "data_analysis": 8.0, "cloud_computing": 6.5,
            "cybersecurity": 3.5, "devops": 6.5, "ui_ux": 3.0,
            "logical_reasoning": 9.0, "problem_solving": 9.0, "mathematics": 8.5,
            "communication": 6.5, "teamwork": 7.0,
            "interest_ai": 9.5, "interest_web": 4.0, "interest_data": 8.5,
            "interest_cybersecurity": 3.5, "interest_cloud": 6.5,
            "interest_software_dev": 7.5, "interest_ui_ux": 3.0, "interest_business": 5.0,
            "pref_style": "Technical"
        },
        "AI Engineer": {
            "python": 9.0, "java": 5.0, "cpp": 7.5, "sql": 6.5, "web_dev": 4.5,
            "machine_learning": 9.0, "data_analysis": 7.5, "cloud_computing": 7.0,
            "cybersecurity": 4.0, "devops": 6.0, "ui_ux": 3.5,
            "logical_reasoning": 9.0, "problem_solving": 9.0, "mathematics": 9.0,
            "communication": 7.0, "teamwork": 7.0,
            "interest_ai": 9.5, "interest_web": 4.0, "interest_data": 8.0,
            "interest_cybersecurity": 4.0, "interest_cloud": 7.0,
            "interest_software_dev": 7.5, "interest_ui_ux": 3.5, "interest_business": 5.0,
            "pref_style": "Technical"
        },
        "Web Developer": {
            "python": 6.0, "java": 4.5, "cpp": 3.0, "sql": 7.0, "web_dev": 9.0,
            "machine_learning": 2.5, "data_analysis": 3.5, "cloud_computing": 5.0,
            "cybersecurity": 4.0, "devops": 5.0, "ui_ux": 7.5,
            "logical_reasoning": 7.5, "problem_solving": 8.0, "mathematics": 6.0,
            "communication": 7.5, "teamwork": 8.0,
            "interest_ai": 4.0, "interest_web": 9.5, "interest_data": 3.5,
            "interest_cybersecurity": 4.0, "interest_cloud": 5.0,
            "interest_software_dev": 8.0, "interest_ui_ux": 8.0, "interest_business": 5.0,
            "pref_style": "Creative"
        },
        "Cybersecurity Analyst": {
            "python": 7.0, "java": 5.5, "cpp": 6.5, "sql": 6.5, "web_dev": 5.0,
            "machine_learning": 4.0, "data_analysis": 5.0, "cloud_computing": 6.5,
            "cybersecurity": 9.2, "devops": 6.0, "ui_ux": 2.5,
            "logical_reasoning": 8.5, "problem_solving": 8.5, "mathematics": 7.0,
            "communication": 7.0, "teamwork": 7.0,
            "interest_ai": 4.5, "interest_web": 5.0, "interest_data": 5.0,
            "interest_cybersecurity": 9.5, "interest_cloud": 6.5,
            "interest_software_dev": 6.0, "interest_ui_ux": 2.5, "interest_business": 5.0,
            "pref_style": "Technical"
        },
        "Cloud Engineer": {
            "python": 7.0, "java": 6.0, "cpp": 4.5, "sql": 6.5, "web_dev": 5.5,
            "machine_learning": 3.5, "data_analysis": 4.5, "cloud_computing": 9.2,
            "cybersecurity": 6.5, "devops": 8.0, "ui_ux": 3.0,
            "logical_reasoning": 8.0, "problem_solving": 8.0, "mathematics": 6.5,
            "communication": 7.0, "teamwork": 7.5,
            "interest_ai": 4.5, "interest_web": 6.0, "interest_data": 5.0,
            "interest_cybersecurity": 6.5, "interest_cloud": 9.5,
            "interest_software_dev": 6.5, "interest_ui_ux": 3.0, "interest_business": 5.5,
            "pref_style": "Technical"
        },
        "DevOps Engineer": {
            "python": 7.5, "java": 6.0, "cpp": 5.0, "sql": 6.0, "web_dev": 6.0,
            "machine_learning": 3.0, "data_analysis": 4.0, "cloud_computing": 8.5,
            "cybersecurity": 6.5, "devops": 9.2, "ui_ux": 3.0,
            "logical_reasoning": 8.5, "problem_solving": 8.5, "mathematics": 6.5,
            "communication": 7.0, "teamwork": 8.0,
            "interest_ai": 4.0, "interest_web": 6.5, "interest_data": 4.0,
            "interest_cybersecurity": 6.5, "interest_cloud": 8.5,
            "interest_software_dev": 7.0, "interest_ui_ux": 3.0, "interest_business": 5.0,
            "pref_style": "Technical"
        },
        "UI/UX Developer": {
            "python": 4.0, "java": 2.5, "cpp": 2.0, "sql": 4.0, "web_dev": 8.5,
            "machine_learning": 2.0, "data_analysis": 3.5, "cloud_computing": 3.0,
            "cybersecurity": 2.0, "devops": 3.0, "ui_ux": 9.5,
            "logical_reasoning": 6.5, "problem_solving": 7.0, "mathematics": 5.0,
            "communication": 8.5, "teamwork": 8.5,
            "interest_ai": 3.5, "interest_web": 8.5, "interest_data": 3.5,
            "interest_cybersecurity": 2.0, "interest_cloud": 3.0,
            "interest_software_dev": 5.5, "interest_ui_ux": 9.5, "interest_business": 6.5,
            "pref_style": "Creative"
        },
        "Business Analyst": {
            "python": 5.0, "java": 2.5, "cpp": 2.0, "sql": 7.5, "web_dev": 3.5,
            "machine_learning": 3.5, "data_analysis": 8.0, "cloud_computing": 4.0,
            "cybersecurity": 3.0, "devops": 3.0, "ui_ux": 6.0,
            "logical_reasoning": 8.0, "problem_solving": 8.0, "mathematics": 7.0,
            "communication": 9.0, "teamwork": 9.0,
            "interest_ai": 4.5, "interest_web": 3.5, "interest_data": 8.0,
            "interest_cybersecurity": 3.0, "interest_cloud": 4.5,
            "interest_software_dev": 4.0, "interest_ui_ux": 6.0, "interest_business": 9.5,
            "pref_style": "Managerial"
        }
    }
    
    records = []
    samples_per_career = num_samples // len(careers)
    
    feature_keys = [
        "python", "java", "cpp", "sql", "web_dev", "machine_learning",
        "data_analysis", "cloud_computing", "cybersecurity", "devops", "ui_ux",
        "logical_reasoning", "problem_solving", "mathematics",
        "communication", "teamwork",
        "interest_ai", "interest_web", "interest_data", "interest_cybersecurity",
        "interest_cloud", "interest_software_dev", "interest_ui_ux", "interest_business"
    ]
    
    for career in careers:
        base = archetypes[career]
        for _ in range(samples_per_career):
            row = {}
            # Generate CGPA between 6.0 and 9.8 with slight noise
            cgpa = np.clip(np.random.normal(loc=7.8, scale=0.8), 6.0, 9.9)
            row["cgpa"] = round(float(cgpa), 2)
            
            for key in feature_keys:
                mean_val = base[key]
                val = np.random.normal(loc=mean_val, scale=1.1)
                val = np.clip(val, 0.0, 10.0)
                row[key] = round(float(val), 1)
                
            # Projects & Certifications
            row["certifications_count"] = int(np.clip(np.random.poisson(lam=1.8), 0, 6))
            row["projects_count"] = int(np.clip(np.random.poisson(lam=2.5), 0, 8))
            row["internship_done"] = int(np.random.choice([0, 1], p=[0.45, 0.55]))
            
            # Work style preference with noise
            work_styles = ["Technical", "Analytical", "Creative", "Managerial"]
            pref = base["pref_style"]
            if np.random.rand() < 0.8:
                row["preferred_work_style"] = pref
            else:
                row["preferred_work_style"] = np.random.choice(work_styles)
                
            row["recommended_career"] = career
            records.append(row)
            
    df = pd.DataFrame(records)
    # Shuffle
    df = df.sample(frac=1.0, random_state=random_state).reset_index(drop=True)
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, "career_dataset.csv")
    df.to_csv(output_file, index=False)
    print(f"[OK] Generated {len(df)} samples saved to {output_file}")
    return df

if __name__ == "__main__":
    generate_career_dataset()
