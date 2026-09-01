# AI-Powered Personalized Career Guidance, Skill Gap Analysis and Learning Recommendation System for Students

> **B.Tech Computer Science & Engineering Final-Year Major Project**  
> Built with Python, Django, Django REST Framework, Scikit-Learn, Pandas, NumPy, pypdf, NLTK, Bootstrap 5, and Chart.js.

---

## 1. Project Abstract

In today’s rapidly evolving tech industry, engineering undergraduates face significant challenges identifying suitable career paths aligned with their aptitude, academic strengths, and technical capabilities. Traditional career counseling platforms rely on static quizzes and hardcoded rule engines. 

This project delivers an intelligent, end-to-end web platform that leverages a **Machine Learning Pipeline (evaluating 6 classification algorithms: Support Vector Machines, Random Forest, Logistic Regression, Gradient Boosting, KNN, Decision Trees)** trained across 20+ academic, programming, aptitude, and interest dimensions to predict top career paths with calibrated suitability scores. Furthermore, the platform integrates an **Automated Skill Gap Analysis Engine** (with interactive Radar and Bar charts), **Personalized Multi-Stage Learning Roadmaps**, **Content-Based Course & Project Recommendations**, an **NLP-based Resume ATS Parser**, an **NLP Mock Interview Simulator** with semantic similarity scoring, and a **Context-Aware Career Chatbot Advisor**.

---

## 2. Key Features

1. **Student Authentication & Academic Profiling**:
   - Secure Django authentication, profile management, CGPA, graduation year, degree, and work style preferences.
   - Interactive 0–10 Technical Skill Rating interface across 35+ industry technologies.

2. **Career Assessment Suite**:
   - Four distinct modules: *Career & Domain Interests*, *Logical & Quantitative Aptitude*, *Core Technical & Programming*, and *Communication & Workplace Soft Skills*.
   - Automated scoring, time limits, question-by-question review with detailed explanations.

3. **Multi-Model Machine Learning Career Prediction Engine**:
   - Evaluates student features against 11 major career tracks (*Software Developer, Data Analyst, Data Scientist, Machine Learning Engineer, AI Engineer, Web Developer, Cybersecurity Analyst, Cloud Engineer, DevOps Engineer, UI/UX Developer, Business Analyst*).
   - Real-time Top-K career predictions with calibrated Suitability Scores.

4. **Interactive Skill Gap Analysis**:
   - Compares student skill ratings against industry benchmarks.
   - Classifies skills into **Strong Competencies**, **Moderate Deficits**, and **Critical Skill Gaps**.
   - Interactive Chart.js Radar Chart visualization.

5. **Personalized Dynamic Learning Roadmap**:
   - Multi-stage learning curriculum customized for the student’s target career.
   - Stage progress tracking (*Not Started*, *In Progress*, *Completed*) with overall percentage completion gauges.

6. **Curated Course & Project Recommendations**:
   - Content-based filtering matching resources and projects directly to the student's identified skill gaps.
   - Project guides with difficulty badges, tech stacks, deliverables, and GitHub starter links.

7. **NLP Resume ATS Analyzer**:
   - Extracts text from uploaded PDF / DOCX resumes using `pypdf` and `docx`.
   - NLP entity heuristics (Email, Phone, Education keywords, Skill extraction).
   - ATS Structure Completeness Score (0-100) and Target Career keyword match percentage.

8. **NLP-Powered Mock Interview Simulator**:
   - Technical, HR, and behavioral interview questions.
   - NLP semantic evaluation using **TF-IDF Cosine Similarity** against reference answers and **Key Concept Keyword Coverage**.
   - Automated performance scorecard with qualitative improvement feedback.

9. **AI Career Advisor Chatbot**:
   - Context-aware virtual career counselor providing instant advice on career paths, next learning steps, interview tips, and project ideas.

10. **Custom Staff & Admin Analytics Dashboard**:
    - Centralized metrics for student enrollment, assessment completion, top target careers, and ML model performance metrics.

---

## 3. System Architecture

```
                                +---------------------------+
                                |      Student / User       |
                                +-------------+-------------+
                                              |
                                              v
                               +-----------------------------+
                               |   Django Web Application    |
                               | (Bootstrap 5 UI + Chart.js) |
                               +--------------+--------------+
                                              |
                     +------------------------+------------------------+
                     |                        |                        |
                     v                        v                        v
        +-------------------------+  +------------------+  +---------------------+
        |  Assessment & Profile   |  | Skill Gap Engine |  |  NLP Engines        |
        |  - Academics (CGPA)     |  | - Radar Data     |  |  - Resume Parser    |
        |  - Skills (0-10)        |  | - Gap Magnitude  |  |  - Interview Eval   |
        |  - Aptitude & Interest  |  | - Strong/Mod/Gap |  |  - Chatbot Advisor  |
        +------------+------------+  +--------+---------+  +----------+----------+
                     |                        |                       |
                     v                        v                       v
        +-------------------------+  +------------------+  +---------------------+
        |   ML Inference Engine   |  | Dynamic Roadmap  |  | Curated Repository  |
        |   - Preprocessor Pipeline| | - Milestone Stg  |  | - Courses / Books   |
        |   - Trained SVM/RF/GB   |  | - Toggle Status  |  | - Capstone Projects |
        |   - Top-K Predictions   |  +------------------+  +---------------------+
        +------------+------------+
                     |
                     v
        +-------------------------+
        |   SQLite / PostgreSQL   |
        +-------------------------+
```

---

## 4. Machine Learning Pipeline & Results

The dataset (`ml_models/dataset/career_dataset.csv`) contains ~3,500 samples spanning 30 features across academic metrics, 11 technical skills, aptitudes, domain interests, certifications, projects, and work styles.

### Model Comparison & Evaluation

| Algorithm | Accuracy | Precision (Weighted) | Recall (Weighted) | F1-Score (Weighted) |
| :--- | :---: | :---: | :---: | :---: |
| **Support Vector Machine (RBF)** | **93.57%** | **93.60%** | **93.57%** | **93.57%** |
| **Logistic Regression** | 92.43% | 92.50% | 92.43% | 92.43% |
| **Random Forest (150 trees)** | 91.43% | 91.43% | 91.43% | 91.42% |
| **Gradient Boosting** | 89.43% | 89.59% | 89.43% | 89.46% |
| **K-Nearest Neighbors (k=7)** | 88.14% | 88.16% | 88.14% | 88.14% |
| **Decision Tree (max_depth=12)**| 78.57% | 79.09% | 78.57% | 78.72% |

The best model (**Support Vector Classifier**) is automatically serialized to `ml_models/model.pkl` along with `ml_models/preprocessor.pkl` and `ml_models/metrics.json`.

---

## 5. Technology Stack

- **Backend**: Python 3.10+, Django 5.x / 6.x, Django REST Framework
- **Machine Learning & NLP**: Scikit-Learn, Pandas, NumPy, Joblib, pypdf, python-docx, NLTK
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5.3, Bootstrap Icons, Chart.js 4.4
- **Database**: SQLite3 (default for local setup; production-ready for PostgreSQL)

---

## 6. Project Directory Structure

```
career_guidance/
¦
+-- manage.py
+-- requirements.txt
+-- README.md
¦
+-- career_guidance_app/
¦   +-- settings.py
¦   +-- urls.py
¦   +-- views.py
¦   +-- tests.py
¦   +-- wsgi.py
¦
+-- accounts/               # Auth, registration, login, logout
+-- students/               # Profile, technical skills (0-10), dashboard
+-- assessments/            # Interest, Aptitude, Technical & Soft skills tests
+-- careers/                # Careers, skill catalog, required benchmarks
+-- recommendations/        # ML inference engine & career recommendation views
+-- skill_gap/              # Skill gap calculations & Radar charts
+-- roadmap/                # Personalized milestone roadmaps
+-- resources/              # Learning courses & documentation repository
+-- projects/               # Practical portfolio project ideas
+-- resume_analyzer/        # PDF resume text extraction & NLP ATS analyzer
+-- interviews/             # Mock interview simulator & NLP semantic evaluator
+-- chatbot/                # Career advisor chatbot
+-- custom_admin/           # Platform analytics & admin management views
¦
+-- ml_models/
¦   +-- dataset/
¦   ¦   +-- generate_dataset.py
¦   ¦   +-- career_dataset.csv
¦   +-- train_model.py      # Multi-model training and evaluation script
¦   +-- model_service.py    # Singleton prediction service
¦   +-- model.pkl           # Serialized trained model
¦   +-- preprocessor.pkl    # Serialized preprocessing pipeline
¦   +-- metrics.json        # Comparative evaluation metrics
¦
+-- templates/              # Responsive HTML templates
+-- static/                 # Custom CSS and JavaScript assets
+-- media/                  # Uploaded resumes
```

---

## 7. Installation & Quickstart

### Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14
- Git (optional)

### Step 1: Clone or Navigate to Project
```bash
cd career_guidance
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Train Machine Learning Models (Optional - Pretrained model included)
```bash
python ml_models/train_model.py
```

### Step 5: Seed Database with Initial Data
Populates 11 careers, 35+ skills, benchmarks, 100+ assessment questions, 50+ learning resources, 30+ projects, and 40+ mock interview questions:
```bash
python manage.py seed_data
```

### Step 6: Create Superuser (Admin) Account
```bash
python manage.py createsuperuser
```
*(Default demo superuser: `admin` / `admin123`)*

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
**`http://127.0.0.1:8000/`**

---

## 8. Step-by-Step User Flow

1. **Register**: Register a new student account at `/accounts/register/`.
2. **Rate Skills**: Rate your technical proficiencies (0 to 10) in Programming, Frameworks, Databases, and Cloud.
3. **Assessments**: Take assessments in Interests, Aptitude, Technical, and Soft Skills.
4. **ML Predictions**: Review your Top ML Career Recommendations with calibrated suitability percentages.
5. **Skill Gap Analysis**: Inspect the interactive Radar Chart for your target career.
6. **Learning Roadmap**: Toggle stages to track your progress (*In Progress* / *Completed*).
7. **Courses & Projects**: Explore courses and project guides filtered for your skill gaps.
8. **Resume ATS Check**: Upload a PDF resume and receive ATS completeness and keyword feedback.
9. **Mock Interview**: Take a simulated technical/HR interview and get instant NLP semantic scores.
10. **Chatbot**: Ask questions anytime to your AI Career Advisor!

---

## 9. Running Automated Tests

Run the automated test suite with:
```bash
python manage.py test
```

---

## 10. Authors & Acknowledgements

- **Project**: AI-Powered Personalized Career Guidance, Skill Gap Analysis and Learning Recommendation System for Students
- **Degree**: Bachelor of Technology (B.Tech) in Computer Science & Engineering
- **Libraries Used**: Django, Scikit-Learn, Pandas, NumPy, pypdf, python-docx, NLTK, Bootstrap 5, Chart.js.
