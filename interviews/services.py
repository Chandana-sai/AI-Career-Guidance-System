import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def evaluate_interview_answer(question, candidate_answer):
    """
    Evaluates candidate answer against reference answer and key concepts using NLP.
    """
    text = candidate_answer.strip()
    words = text.split()
    word_count = len(words)
    
    if word_count < 5:
        return {
            "nlp_score": 15.0,
            "similarity_score": 5.0,
            "keyword_coverage": 0.0,
            "word_count": word_count,
            "matched_keywords": [],
            "missing_keywords": question.get_keywords_list(),
            "feedback": "Answer is too brief. Please provide a detailed technical explanation with clear reasoning and examples."
        }
        
    text_lower = text.lower()
    
    # 1. Key Concept Coverage
    key_concepts = question.get_keywords_list()
    matched_keys = []
    missing_keys = []
    
    for kc in key_concepts:
        # Check if keyword or parts appear in answer
        if kc in text_lower:
            matched_keys.append(kc)
        else:
            # Check individual sub-words for multi-word concepts
            sub_words = kc.split()
            if len(sub_words) > 1 and all(sw in text_lower for sw in sub_words):
                matched_keys.append(kc)
            else:
                missing_keys.append(kc)
                
    coverage_pct = 0.0
    if key_concepts:
        coverage_pct = round((len(matched_keys) / len(key_concepts)) * 100.0, 1)
        
    # 2. TF-IDF Cosine Similarity
    ref_text = question.reference_answer
    sim_score = 0.0
    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform([text, ref_text])
        cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        sim_score = round(float(cos_sim) * 100.0, 1)
    except Exception:
        sim_score = coverage_pct
        
    # 3. Depth Factor
    depth_multiplier = 1.0
    if word_count < 25:
        depth_multiplier = 0.75
    elif word_count > 150:
        depth_multiplier = 1.05
        
    # 4. Aggregated Score
    # 50% keyword coverage + 50% semantic cosine similarity, scaled by depth
    weighted_score = (0.50 * coverage_pct) + (0.50 * sim_score)
    final_score = min(98.0, max(20.0, round(weighted_score * depth_multiplier, 1)))
    
    # 5. Feedback generation
    feedback_points = []
    if final_score >= 80:
        feedback_points.append("Excellent answer! You demonstrated strong conceptual clarity and covered key technical terminology.")
    elif final_score >= 60:
        feedback_points.append("Good response! You addressed the core concept but could deepen the technical explanation.")
    else:
        feedback_points.append("Needs improvement. The response is either missing fundamental technical terms or lacks depth.")
        
    if missing_keys:
        missing_str = ", ".join(missing_keys[:4])
        feedback_points.append(f"Important concepts to touch upon: **{missing_str}**.")
        
    if word_count < 35:
        feedback_points.append("Tip: In real interviews, use the STAR approach or give specific practical code examples.")
        
    return {
        "nlp_score": final_score,
        "similarity_score": sim_score,
        "keyword_coverage": coverage_pct,
        "word_count": word_count,
        "matched_keywords": matched_keys,
        "missing_keywords": missing_keys,
        "feedback": " \n".join(feedback_points)
    }
