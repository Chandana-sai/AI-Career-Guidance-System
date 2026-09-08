from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
import os

from students.models import StudentProfile, StudentSkill
from careers.models import Career, Skill, CareerSkill
from assessments.models import AssessmentCategory, Question, AssessmentSession
from roadmap.models import RoadmapTemplate, RoadmapStage, StudentRoadmapProgress
from resume_analyzer.services import analyze_resume_content
from interviews.models import InterviewQuestion, InterviewSession
from interviews.services import evaluate_interview_answer
from ml_models.model_service import CareerModelService
from skill_gap.services import calculate_skill_gap
from chatbot.services import generate_bot_response

class CareerMatePlatformTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create user & profile
        self.user = User.objects.create_user(
            username="student_test",
            email="student@test.com",
            password="testpassword123",
            first_name="Chandana",
            last_name="Reddy"
        )
        
        # Seed skills
        self.py_skill = Skill.objects.create(name="Python", category="Programming")
        self.ml_skill = Skill.objects.create(name="Machine Learning", category="Domain")
        self.sql_skill = Skill.objects.create(name="SQL", category="Database")
        
        # Seed career
        self.career_ds = Career.objects.create(
            title="Data Scientist",
            category="Data & Analytics",
            description="Analyzes complex data.",
            average_salary="₹9 - ₹22 LPA"
        )
        self.career_sd = Career.objects.create(
            title="Software Developer",
            category="Software Engineering",
            description="Builds applications.",
            average_salary="₹7 - ₹18 LPA"
        )
        
        CareerSkill.objects.create(career=self.career_ds, skill=self.py_skill, required_level=8.5, weight=1.0)
        CareerSkill.objects.create(career=self.career_ds, skill=self.ml_skill, required_level=8.0, weight=1.2)
        CareerSkill.objects.create(career=self.career_ds, skill=self.sql_skill, required_level=7.5, weight=1.0)
        
        self.profile = StudentProfile.objects.create(
            user=self.user,
            cgpa=8.5,
            target_career=self.career_ds
        )
        
        StudentSkill.objects.create(student=self.profile, skill=self.py_skill, proficiency_level=9.0) # Strong
        StudentSkill.objects.create(student=self.profile, skill=self.sql_skill, proficiency_level=5.0) # Moderate
        StudentSkill.objects.create(student=self.profile, skill=self.ml_skill, proficiency_level=0.0) # Gap

    def test_user_authentication(self):
        login_success = self.client.login(username="student_test", password="testpassword123")
        self.assertTrue(login_success)
        response = self.client.get(reverse("students:dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_skill_gap_calculation(self):
        gap_res = calculate_skill_gap(self.profile, self.career_ds)
        self.assertIsNotNone(gap_res)
        self.assertEqual(gap_res["strong_count"], 1)
        self.assertEqual(gap_res["moderate_count"], 1)
        self.assertEqual(gap_res["gap_count"], 1)
        self.assertGreater(gap_res["readiness_percentage"], 0.0)
        self.assertIn("Python", gap_res["radar_chart"]["labels"])

    def test_ml_model_service_prediction(self):
        service = CareerModelService()
        input_data = {
            "cgpa": 8.5,
            "python": 9.0,
            "machine_learning": 8.5,
            "data_analysis": 8.0,
            "sql": 8.0,
            "logical_reasoning": 8.0,
            "problem_solving": 8.5,
            "preferred_work_style": "Analytical"
        }
        res = service.predict(input_data, top_n=3)
        self.assertIn("top_recommendations", res)
        self.assertGreater(len(res["top_recommendations"]), 0)
        top_rec = res["top_recommendations"][0]
        self.assertIn("career", top_rec)
        self.assertIn("calibrated_score", top_rec)
        self.assertGreaterEqual(top_rec["calibrated_score"], 60.0)

    def test_roadmap_stage_generation_and_toggle(self):
        template = RoadmapTemplate.objects.create(
            career=self.career_ds,
            title="Data Science Roadmap",
            estimated_months=6
        )
        stage = RoadmapStage.objects.create(
            template=template,
            stage_number=1,
            title="Stage 1: Python & Statistics",
            estimated_weeks=4
        )
        
        self.client.login(username="student_test", password="testpassword123")
        resp = self.client.post(reverse("roadmap:toggle_stage", args=[stage.id]), {"status": "Completed"})
        self.assertEqual(resp.status_code, 302)
        
        prog = StudentRoadmapProgress.objects.get(student=self.profile, stage=stage)
        self.assertEqual(prog.status, "Completed")
        self.assertIsNotNone(prog.completed_at)

    def test_resume_nlp_analysis(self):
        sample_resume_text = """
        Chandana Reddy
        Email: chandana@example.com | Phone: (555) 123-4567
        Education: B.Tech in Computer Science and Engineering, CGPA 8.5
        Technical Skills: Python, SQL, Git, Linux, Docker, Machine Learning
        Projects: E-Commerce Analytics Web App with Django and PostgreSQL
        Experience: Software Engineering Intern at Tech Corp
        """
        analysis = analyze_resume_content(sample_resume_text, self.career_ds)
        self.assertEqual(analysis["email"], "chandana@example.com")
        self.assertIn("Python", analysis["detected_skills"])
        self.assertIn("SQL", analysis["detected_skills"])
        self.assertGreater(analysis["completeness_score"], 70.0)

    def test_interview_nlp_evaluation(self):
        q = InterviewQuestion.objects.create(
            career=self.career_ds,
            category="Technical",
            difficulty="Medium",
            question_text="What is the difference between Supervised and Unsupervised Learning?",
            reference_answer="Supervised learning trains on labeled datasets where ground truth target labels are provided to predict outcomes like classification and regression. Unsupervised learning analyzes unlabeled data to uncover hidden patterns, representations, and clusters without predefined ground truth.",
            key_concepts="labeled, unlabeled, target labels, classification, regression, clusters, patterns"
        )
        candidate_ans = "Supervised learning uses labeled datasets with target labels to train classification or regression models. In contrast, unsupervised learning works on unlabeled data to find hidden clusters and patterns."
        
        eval_res = evaluate_interview_answer(q, candidate_ans)
        self.assertGreaterEqual(eval_res["nlp_score"], 65.0)
        self.assertGreaterEqual(eval_res["keyword_coverage"], 60.0)
        self.assertIn("feedback", eval_res)

    def test_multilingual_chatbot_responses(self):
        # English
        reply_en, chips_en = generate_bot_response("Which career is good for me?", self.profile, lang="en")
        self.assertIn("recommendations", reply_en.lower())
        self.assertIn("What career suits me?", chips_en)
        
        # Telugu
        reply_te, chips_te = generate_bot_response("కెరీర్ సిఫార్సులు", self.profile, lang="te")
        self.assertTrue(len(reply_te) > 10)
        
        # Hindi
        reply_hi, chips_hi = generate_bot_response("करियर विकल्प", self.profile, lang="hi")
        self.assertTrue(len(reply_hi) > 10)
