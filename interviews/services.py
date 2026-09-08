import re
import math
from collections import Counter

def _tokenize(text):
    # Lowercase and split on non-alphanumeric characters
    tokens = re.findall(r"\b[a-z0-9]+\b", text.lower())
    # English stop words list
    stop_words = {
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
        "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
        "below", "between", "both", "but", "by", "can", "cannot", "could", "couldn't",
        "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
        "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
        "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
        "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
        "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
        "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
        "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
        "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
        "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
        "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
        "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
        "they've", "this", "those", "through", "to", "too", "under", "until", "up",
        "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
        "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
        "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
        "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
        "yourself", "yourselves"
    }
    return [t for t in tokens if t not in stop_words and len(t) > 1]

def _compute_tfidf_cosine_similarity(text1, text2):
    tokens1 = _tokenize(text1)
    tokens2 = _tokenize(text2)
    
    if not tokens1 or not tokens2:
        return 0.0
        
    counts1 = Counter(tokens1)
    counts2 = Counter(tokens2)
    
    vocab = list(set(counts1.keys()).union(set(counts2.keys())))
    
    # Compute TF-IDF weights (2 documents)
    vec1 = []
    vec2 = []
    for word in vocab:
        tf1 = counts1.get(word, 0) / len(tokens1)
        tf2 = counts2.get(word, 0) / len(tokens2)
        # Document frequency
        df = (1 if word in counts1 else 0) + (1 if word in counts2 else 0)
        idf = math.log((2.0 + 1.0) / (df + 1.0)) + 1.0
        
        vec1.append(tf1 * idf)
        vec2.append(tf2 * idf)
        
    # Cosine Similarity
    dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
    mag1 = math.sqrt(sum(v1 ** 2 for v1 in vec1))
    mag2 = math.sqrt(sum(v2 ** 2 for v2 in vec2))
    
    if mag1 == 0 or mag2 == 0:
        return 0.0
        
    return dot_product / (mag1 * mag2)

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
        if kc in text_lower:
            matched_keys.append(kc)
        else:
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
    sim_ratio = _compute_tfidf_cosine_similarity(text, ref_text)
    sim_score = round(float(sim_ratio) * 100.0, 1)
        
    # 3. Depth Factor
    depth_multiplier = 1.0
    if word_count < 25:
        depth_multiplier = 0.75
    elif word_count > 150:
        depth_multiplier = 1.05
        
    # 4. Aggregated Score
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
