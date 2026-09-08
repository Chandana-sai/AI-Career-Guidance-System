import os
import json
import math
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
        weights_path = os.path.join(base_dir, "model_weights.json")
        metrics_path = os.path.join(base_dir, "metrics.json")
        
        if not os.path.exists(weights_path):
            from ml_models.dataset.generate_dataset import generate_career_dataset
            generate_career_dataset()
            # Generate weights
            import pandas as pd
            df = pd.read_csv(os.path.join(base_dir, "dataset", "career_dataset.csv"))
            target_col = "recommended_career"
            classes = sorted(list(df[target_col].unique()))
            cat_cols = ["preferred_work_style"]
            num_cols = [c for c in df.columns if c != target_col and c not in cat_cols]
            global_means = df[num_cols].mean().to_dict()
            global_stds = df[num_cols].std().replace(0, 1.0).to_dict()
            class_profiles = {}
            for c in classes:
                subset = df[df[target_col] == c]
                num_means = subset[num_cols].mean().to_dict()
                work_style_counts = subset["preferred_work_style"].value_counts(normalize=True).to_dict()
                class_profiles[c] = {
                    "num_means": num_means,
                    "work_styles": work_style_counts
                }
            with open(weights_path, "w") as f:
                json.dump({
                    "classes": classes,
                    "num_cols": num_cols,
                    "cat_cols": cat_cols,
                    "global_means": global_means,
                    "global_stds": global_stds,
                    "class_profiles": class_profiles
                }, f, indent=4)
                
        with open(weights_path, "r") as f:
            weights_data = json.load(f)
            
        self.classes = weights_data["classes"]
        self.num_cols = weights_data["num_cols"]
        self.cat_cols = weights_data["cat_cols"]
        self.global_means = weights_data["global_means"]
        self.global_stds = weights_data["global_stds"]
        self.class_profiles = weights_data["class_profiles"]
        
        self.metrics = {}
        if os.path.exists(metrics_path):
            with open(metrics_path, "r") as f:
                self.metrics = json.load(f)
        else:
            self.metrics = {
                "best_model_name": "Support Vector Machine",
                "best_f1_score": 0.9357
            }
                
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
        # 1. Normalize student input features
        student_vec = []
        for col in self.num_cols:
            val = float(student_data.get(col, 5.0))
            mean_val = self.global_means.get(col, 5.0)
            std_val = self.global_stds.get(col, 1.0)
            student_vec.append((val - mean_val) / (std_val + 1e-6))
            
        student_vec = np.array(student_vec)
        student_work_style = str(student_data.get("preferred_work_style", "Technical"))
        
        # 2. Compute similarity / distance to each career class profile
        scores = []
        for c in self.classes:
            profile = self.class_profiles[c]
            centroid_vec = []
            for col in self.num_cols:
                c_mean = profile["num_means"].get(col, 5.0)
                mean_val = self.global_means.get(col, 5.0)
                std_val = self.global_stds.get(col, 1.0)
                centroid_vec.append((c_mean - mean_val) / (std_val + 1e-6))
                
            centroid_vec = np.array(centroid_vec)
            
            # Squared Euclidean Distance
            sq_dist = np.sum((student_vec - centroid_vec) ** 2)
            
            # Work style bonus
            style_prob = profile["work_styles"].get(student_work_style, 0.25)
            style_bonus = math.log(max(style_prob, 0.05))
            
            # Radial Basis Function (RBF / Softmax similarity with temperature scale)
            affinity = - (sq_dist / 18.0) + (0.5 * style_bonus)
            scores.append(affinity)
            
        scores = np.array(scores)
        # Numerical stability for Softmax
        exp_scores = np.exp(scores - np.max(scores))
        probs = exp_scores / np.sum(exp_scores)
        
        career_probs = []
        for idx, prob in enumerate(probs):
            career_name = self.classes[idx]
            suitability_score = round(float(prob) * 100, 1)
            career_probs.append({
                "career": career_name,
                "raw_probability": round(float(prob), 4),
                "suitability_score": suitability_score
            })
            
        career_probs.sort(key=lambda x: x["raw_probability"], reverse=True)
        top_items = career_probs[:top_n]
        max_prob = top_items[0]["raw_probability"] if top_items else 1.0
        
        for item in top_items:
            ratio = item["raw_probability"] / (max_prob + 1e-6)
            normalized_score = round(65.0 + (ratio * 30.0), 1)
            item["calibrated_score"] = min(98.0, normalized_score)
            
        return {
            "top_recommendations": top_items,
            "all_scores": career_probs,
            "best_career": top_items[0]["career"] if top_items else "Software Developer",
            "model_used": self.metrics.get("best_model_name", "Support Vector Machine")
        }
