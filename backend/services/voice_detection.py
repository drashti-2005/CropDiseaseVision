import os
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Get the base directory path properly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "disease_symptoms.json")

# Initialize the NLP components
# Use n-grams (1 to 3 words) to capture symptom phrases better
vectorizer = TfidfVectorizer(stop_words='english', lowercase=True, ngram_range=(1, 3))
disease_names = []
disease_symptoms_corpus = []
tfidf_matrix = None

def init_nlp_model():
    """Load the symptom database and fit the TF-IDF vectorizer."""
    global disease_names, disease_symptoms_corpus, tfidf_matrix
    
    try:
        with open(DATA_PATH, 'r') as f:
            data = json.load(f)
            
        for disease, symptoms in data.items():
            disease_names.append(disease)
            # Combine the disease name and symptoms for better matching
            disease_clean = disease.replace('___', ' ').replace('_', ' ')
            combined_symptoms = disease_clean + " " + " ".join(symptoms)
            disease_symptoms_corpus.append(combined_symptoms)
            
        # Fit and transform the corpus into TF-IDF vectors
        tfidf_matrix = vectorizer.fit_transform(disease_symptoms_corpus)
        print(f"[OK] Voice NLP Model initialized with {len(disease_names)} classes.")
    except Exception as e:
        print(f"[ERROR] Failed to initialize Voice NLP Model: {e}")

# Initialize when the module loads
init_nlp_model()

def predict_disease_from_text(text):
    """
    Given a text description of symptoms, predict the disease using TF-IDF and Cosine Similarity.
    """
    if not text or not text.strip():
        return "Unknown", 0.0
        
    if tfidf_matrix is None:
        print("[ERROR] NLP Model is not initialized.")
        return "Unknown", 0.0
        
    # Transform the input text into a vector
    input_vector = vectorizer.transform([text])
    
    # Calculate cosine similarity against all known disease symptom vectors
    similarities = cosine_similarity(input_vector, tfidf_matrix)
    
    # Get the index of the highest similarity score
    best_match_idx = np.argmax(similarities)
    best_score = similarities[0][best_match_idx]
    
    # Get second-best score for comparison (to check if it's a confident match)
    similarities_flat = similarities[0].flatten()
    sorted_scores = np.sort(similarities_flat)
    second_best_score = sorted_scores[-2] if len(sorted_scores) > 1 else 0
    
    # Extract the corresponding disease name
    disease_name = disease_names[best_match_idx]
    
    # Enhanced confidence validation
    MINIMUM_THRESHOLD = 0.35  # Require at least 35% similarity (increased from 0.05)
    RELATIVE_THRESHOLD = 0.15  # Best score must be at least 15% higher than second-best
    
    print(f"[VOICE] Input: '{text}' | Best: {best_score:.3f} | Second: {second_best_score:.3f} | Disease: {disease_name}")
    
    # If the score is below minimum threshold, reject it
    if best_score < MINIMUM_THRESHOLD:
        print(f"[VOICE] ✗ REJECTED - Below minimum threshold ({best_score:.3f} < {MINIMUM_THRESHOLD})")
        return "Unknown", 0.0
    
    # Check if there's a significant gap between best and second-best (to avoid ambiguous matches)
    score_difference = best_score - second_best_score
    if score_difference < RELATIVE_THRESHOLD:
        print(f"[VOICE] ✗ REJECTED - Too similar to alternatives ({score_difference:.3f} < {RELATIVE_THRESHOLD})")
        return "Unknown", 0.0
    
    print(f"[VOICE] ✓ ACCEPTED - Confident match ({best_score:.3f})")
    return disease_name, float(best_score)
