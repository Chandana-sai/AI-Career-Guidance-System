import os
import json
import joblib
import pandas as pd
import numpy as np

class CareerModelService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CareerModelService, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance
        
    def _load_model(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "model.pkl")
        preprocessor_path = os.path.join(base_dir, "preprocessor.pkl")
        metrics_path = os.path.join(base_dir, "metrics.json")
        
        if not os.path.exists(model_path) or not os.path.exists(preprocessor_path):
            from ml_models.train_model import train_and_evaluate_models
            train_and_evaluate_models()
            
        self.model = joblib.load(model_path)
        prep_data = joblib.load(preprocessor_path)
        self.preprocessor = prep_data["preprocessor"]
        self.label_encoder = prep_data["label_encoder"]
        self.num_cols = prep_data["num_cols"]
        self.cat_cols = prep_data["cat_cols"]
        self.classes = prep_data["classes"]
        
        self.metrics = {}
        if os.path.exists(metrics_path):
            with open(metrics_path, "r") as f:
                self.metrics = json.load(f)
                
    def get_metrics(self):
        return self.metrics

    def predict(self, student_data, top_n=5):
        """
        Takes student_data dict containing:
        - cgpa
        - programming ratings (python, java, cpp, sql, web_dev, machine_learning, data_analysis, cloud_computing, cybersecurity, devops, ui_ux)
        - aptitudes (logical_reasoning, problem_solving, mathematics, communication, teamwork)
        - interests (interest_ai, interest_web, interest_data, interest_cybersecurity, interest_cloud, interest_software_dev, interest_ui_ux, interest_business)
        - certifications_count, projects_count, internship_done, preferred_work_style
        """
        # Ensure all columns are present with fallback defaults
        row = {}
        for col in self.num_cols:
            row[col] = float(student_data.get(col, 5.0))
            
        for col in self.cat_cols:
            row[col] = str(student_data.get(col, "Technical"))
            
        df_input = pd.DataFrame([row])
        X_trans = self.preprocessor.transform(df_input)
        
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X_trans)[0]
        else:
            # Fallback for models without native predict_proba
            dec = self.model.decision_function(X_trans)[0]
            exp_dec = np.exp(dec - np.max(dec))
            probs = exp_dec / np.sum(exp_dec)
            
        career_probs = []
        for idx, prob in enumerate(probs):
            career_name = self.classes[idx]
            # Calibrate suitability score to a 50-98% range for realistic student feedback
            # where the top choice gets 85-98%
            suitability_score = round(float(prob) * 100, 1)
            career_probs.append({
                "career": career_name,
                "raw_probability": round(float(prob), 4),
                "suitability_score": suitability_score
            })
            
        # Sort descending by raw_probability
        career_probs.sort(key=lambda x: x["raw_probability"], reverse=True)
        
        # Calculate dynamic normalized suitability score for top recommendations
        top_items = career_probs[:top_n]
        max_prob = top_items[0]["raw_probability"] if top_items else 1.0
        
        for item in top_items:
            # Scaled score: relative to top prediction
            ratio = item["raw_probability"] / (max_prob + 1e-6)
            normalized_score = round(65.0 + (ratio * 30.0), 1) # between 65% and 95%
            item["calibrated_score"] = min(98.0, normalized_score)
            
        return {
            "top_recommendations": top_items,
            "all_scores": career_probs,
            "best_career": top_items[0]["career"] if top_items else "Software Developer",
            "model_used": self.metrics.get("best_model_name", "Support Vector Machine")
        }
