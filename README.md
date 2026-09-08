# CareerMate – AI Student Career Guidance and Resume Assistant

> **B.Tech Computer Science & Engineering Final-Year Project**  
> Built with Python, Django, Django REST Framework, Scikit-Learn, Pandas, NumPy, pypdf, NLTK, Bootstrap 5, Chart.js, and the Web Speech API (Voice & Multilingual).

---

## 1. Project Abstract

In today’s fast-moving software and engineering landscape, students often face confusion selecting the right career path, improving their resumes, identifying skill gaps, and preparing for interviews. 

**CareerMate** is a friendly, modern, and intelligent career companion built specifically for engineering undergraduates. It provides:
1. **AI Career Guidance**: Evaluates academic performance, 0–10 programming skill ratings, and aptitude assessments using a trained Machine Learning model to predict suitable career tracks (*High Match*, *Good Match*, *Moderate Match*).
2. **Skill Gap Analyzer**: Benchmarks current student proficiencies against industry requirements using interactive **Radar** and **Bar charts**, classifying skills into *Strong*, *Skills to Improve*, and *Missing Skills*.
3. **NLP Resume ATS Analyzer**: Extracts text from PDF/DOCX resumes, computes an automated ATS score (0–100), extracts detected/missing skills, highlights resume strengths, provides numbered improvement suggestions, and shows multi-career match percentages with printable report downloads.
4. **Friendly AI CareerMate Chatbot (Text & Voice)**: A friendly senior-style virtual counselor supporting **English, Telugu (తెలుగు), and Hindi (हिंदी)** with **Speech-to-Text (Voice Input 🎤)** and **Text-to-Speech (Voice Output 🔊)**.
5. **Personalized Learning Roadmap**: Milestone-based stages with interactive *Not Started / In Progress / Completed* status toggles and progress gauges.
6. **Interview Preparation**: Practice Technical, HR, and Behavioral questions with instant NLP semantic scoring and qualitative feedback.

---

## 2. Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Bootstrap Icons, Chart.js 4.4, Web Speech Recognition & SpeechSynthesis APIs.
- **Backend**: Python 3.10+, Django, Django REST Framework.
- **Machine Learning & NLP**: Scikit-Learn, Pandas, NumPy, pypdf, python-docx, NLTK, pure Python TF-IDF and Cosine Similarity.
- **Database**: SQLite3 (default for zero-setup local development; PostgreSQL compatible).

---

## 3. How to Run the Project

### Step 1: Navigate to Project Directory
```powershell
cd C:\Users\chand\.gemini\antigravity\scratch\career_guidance
```

### Step 2: Start the Development Server
```powershell
python manage.py runserver
```

Open your browser and navigate to:
**`http://127.0.0.1:8000/`**

### Pre-Configured Demo Accounts:
- **Admin / Staff Account**:
  - **Username**: `admin`
  - **Password**: `admin123`
- **Student Account**:
  - Register a new account at `http://127.0.0.1:8000/accounts/register/` or login with `student_test` / `testpassword123`.

---

## 4. Running Automated Tests

Run the automated test suite with:
```powershell
python manage.py test
```
*Result: 7/7 tests passing (100% OK).*
