import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

from dataset.generate_dataset import generate_career_dataset

def train_and_evaluate_models():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, "dataset", "career_dataset.csv")
    
    if not os.path.exists(dataset_path):
        print("Dataset not found. Generating fresh dataset...")
        df = generate_career_dataset(num_samples=3500)
    else:
        df = pd.read_csv(dataset_path)
        
    print(f"Loaded dataset shape: {df.shape}")
    
    # Target and Features
    target_col = "recommended_career"
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Encode target
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    classes = list(label_encoder.classes_)
    
    # Identify feature types
    cat_cols = ["preferred_work_style"]
    num_cols = [c for c in X.columns if c not in cat_cols]
    
    # Preprocessor pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols)
        ]
    )
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    X_train_trans = preprocessor.fit_transform(X_train)
    X_test_trans = preprocessor.transform(X_test)
    
    # Extract transformed feature names
    cat_encoder = preprocessor.named_transformers_["cat"]
    cat_feature_names = list(cat_encoder.get_feature_names_out(cat_cols))
    all_feature_names = num_cols + cat_feature_names
    
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=12, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=150, max_depth=15, random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=7),
        "Support Vector Machine": SVC(probability=True, kernel="rbf", C=1.0, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
    }
    
    results = {}
    best_model_name = None
    best_f1 = -1.0
    best_model = None
    
    print("\n--- Training and Evaluating Models ---")
    for name, clf in models.items():
        print(f"Training {name}...")
        clf.fit(X_train_trans, y_train)
        y_pred = clf.predict(X_test_trans)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
        
        cm = confusion_matrix(y_test, y_pred).tolist()
        
        results[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "confusion_matrix": cm
        }
        
        print(f"  Accuracy:  {acc*100:.2f}% | F1: {f1*100:.2f}% | Precision: {prec*100:.2f}% | Recall: {rec*100:.2f}%")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_model = clf
            
    print(f"\n[BEST MODEL]: {best_model_name} with Weighted F1 Score: {best_f1*100:.2f}%")
    
    # Save artifacts
    model_path = os.path.join(base_dir, "model.pkl")
    preprocessor_path = os.path.join(base_dir, "preprocessor.pkl")
    metrics_path = os.path.join(base_dir, "metrics.json")
    
    metadata = {
        "best_model_name": best_model_name,
        "best_f1_score": round(float(best_f1), 4),
        "classes": classes,
        "num_cols": num_cols,
        "cat_cols": cat_cols,
        "feature_names": all_feature_names,
        "models_comparison": results
    }
    
    joblib.dump(best_model, model_path)
    joblib.dump({
        "preprocessor": preprocessor,
        "label_encoder": label_encoder,
        "num_cols": num_cols,
        "cat_cols": cat_cols,
        "classes": classes
    }, preprocessor_path)
    
    with open(metrics_path, "w") as f:
        json.dump(metadata, f, indent=4)
        
    print(f"[OK] Saved model to {model_path}")
    print(f"[OK] Saved preprocessor to {preprocessor_path}")
    print(f"[OK] Saved metrics to {metrics_path}")
    return metadata

if __name__ == "__main__":
    train_and_evaluate_models()
