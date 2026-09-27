"""
Enhanced Voice-Based Disease Detection Assistant
Integrates voice input with disease detection and provides detailed responses
"""

import json
import os
from typing import Dict, Optional, Tuple
from backend.services.chat_assistant_service import process_farmer_question
from backend.services.translation_service import translate_text

# Disease symptom database
DISEASE_SYMPTOMS_DB = {
    "Apple___Apple_scab": {
        "leaf_type": "Apple",
        "disease": "Apple Scab",
        "symptoms": ["dark scabby lesions", "olive-brown spots", "cork-like texture", "misshapen fruit"],
        "causes": "Fungal infection (Venturia inaequalis)",
        "environment": "wet, cool weather",
        "treatment": [
            "Remove and destroy infected leaves",
            "Apply Captan or Mancozeb fungicide early season",
            "Improve air circulation by pruning",
            "Avoid overhead watering"
        ],
        "prevention": ["Remove fallen leaves in autumn", "Apply preventative fungicides in spring"]
    },
    "Apple___Black_rot": {
        "leaf_type": "Apple",
        "disease": "Black Rot",
        "symptoms": ["black circular spots", "concentric rings", "dead tissue", "hard lesions"],
        "causes": "Fungal infection (Phyllosticta mali)",
        "environment": "warm, humid conditions",
        "treatment": [
            "Prune infected branches",
            "Apply copper fungicide",
            "Remove infected fruit from tree and ground"
        ],
        "prevention": ["Maintain tree health", "Improve drainage"]
    },
    "Potato___Early_blight": {
        "leaf_type": "Potato",
        "disease": "Early Blight",
        "symptoms": ["target-like concentric rings", "brown spots on older leaves", "yellowing", "lesions start at bottom"],
        "causes": "Fungal spores (Alternaria solani)",
        "environment": "warm, wet weather",
        "treatment": [
            "Remove infected lower leaves",
            "Apply copper-based fungicide or Chlorothalonil",
            "Mulch the base of plants",
            "Ensure good air circulation"
        ],
        "prevention": ["Use crop rotation (3-4 years)", "Plant resistant varieties", "Avoid overhead watering"]
    },
    "Potato___Late_blight": {
        "leaf_type": "Potato",
        "disease": "Late Blight",
        "symptoms": ["water-soaked spots", "rapid decay", "white fuzz on underside", "black stem rot", "fast spread"],
        "causes": "Oomycete pathogen (Phytophthora infestans)",
        "environment": "cool, wet conditions",
        "treatment": [
            "Destroy infected plants immediately",
            "Apply Metalaxyl or Mefenoxam fungicide",
            "Isolate infected plants from healthy ones",
            "Apply fungicide every 7-10 days if needed"
        ],
        "prevention": ["Plant resistant varieties", "Use crop rotation", "Remove volunteer potatoes"]
    },
    "Tomato___Early_blight": {
        "leaf_type": "Tomato",
        "disease": "Early Blight",
        "symptoms": ["target-like brown spots", "concentric rings", "starts on lower leaves", "spreads upward"],
        "causes": "Fungal infection (Alternaria solani)",
        "environment": "warm, humid weather",
        "treatment": [
            "Remove infected leaves (especially lower ones)",
            "Apply fungicide (Mancozeb, Chlorothalonil)",
            "Stake plants for air circulation",
            "Water at soil level only"
        ],
        "prevention": ["Mulch to prevent soil splash", "Avoid overhead watering", "Remove fallen leaves"]
    },
    "Tomato___Late_blight": {
        "leaf_type": "Tomato",
        "disease": "Late Blight",
        "symptoms": ["water-soaked spots", "tan to brown lesions", "white mold on underside", "green fruit rot"],
        "causes": "Oomycete pathogen (Phytophthora infestans)",
        "environment": "cool, wet conditions",
        "treatment": [
            "Remove and destroy infected plants",
            "Apply Metalaxyl fungicide",
            "Ensure good air circulation",
            "Apply fungicide preventatively in cool seasons"
        ],
        "prevention": ["Use resistant varieties", "Avoid overhead watering", "Space plants properly"]
    },
    "Tomato___Bacterial_spot": {
        "leaf_type": "Tomato",
        "disease": "Bacterial Spot",
        "symptoms": ["small water-soaked spots", "yellow halo around spots", "appears on fruit too", "spots enlarge slowly"],
        "causes": "Bacterial infection (Xanthomonas species)",
        "environment": "warm, wet conditions",
        "treatment": [
            "Spray copper bactericide",
            "Remove infected leaves and fruit",
            "Avoid overhead watering",
            "Sanitize tools between plants"
        ],
        "prevention": ["Use certified disease-free seeds", "Practice crop rotation", "Remove infected debris"]
    },
    "Corn_(maize)___Common_rust_": {
        "leaf_type": "Corn/Maize",
        "disease": "Common Rust",
        "symptoms": ["reddish-brown pustules", "appear on both leaf surfaces", "looks like raised bumps", "leaves may dry early"],
        "causes": "Fungal infection (Puccinia sorghi)",
        "environment": "mild, humid weather",
        "treatment": [
            "Use rust-resistant corn varieties",
            "Apply foliar fungicides early if needed",
            "Remove infected leaves if severe"
        ],
        "prevention": ["Plant resistant varieties", "Plant early", "Space plants for air circulation"]
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "leaf_type": "Corn/Maize",
        "disease": "Northern Leaf Blight",
        "symptoms": ["long, narrow lesions", "gray center with dark border", "cigar-shaped spots", "starts on lower leaves"],
        "causes": "Fungal infection (Setosphaeria turcica)",
        "environment": "cool, wet weather",
        "treatment": [
            "Use resistant hybrids",
            "Apply fungicide if needed",
            "Improve air circulation"
        ],
        "prevention": ["Plant resistant varieties", "Crop rotation", "Remove crop residue"]
    }
}

def detect_leaf_and_disease_from_voice(user_query: str) -> Dict:
    """
    Analyze user voice input to identify leaf type and disease mentioned.
    
    Args:
        user_query: Text transcribed from user voice
    
    Returns:
        Dict with detected leaf type, disease, confidence, and detailed info
    """
    query_lower = user_query.lower()
    best_match = None
    best_score = 0
    
    # Search through disease database
    for class_name, disease_info in DISEASE_SYMPTOMS_DB.items():
        score = 0
        
        # Check for exact disease name match
        disease_lower = disease_info["disease"].lower()
        if disease_lower in query_lower:
            score += 100
        
        # Check for leaf type match
        leaf_lower = disease_info["leaf_type"].lower()
        if leaf_lower in query_lower:
            score += 50
        
        # Check for symptom keywords
        for symptom in disease_info["symptoms"]:
            if symptom.lower() in query_lower:
                score += 30
        
        # Check for disease keywords
        for keyword in ["blight", "rust", "scab", "spot", "rot", "mold", "fungal", "bacterial"]:
            if keyword in query_lower:
                if keyword in disease_lower:
                    score += 20
        
        if score > best_score:
            best_score = score
            best_match = (class_name, disease_info)
    
    # Calculate confidence
    confidence = min(best_score / 100, 1.0)
    
    if best_match and confidence > 0.3:
        class_name, disease_info = best_match
        return {
            "detected": True,
            "leaf_type": disease_info["leaf_type"],
            "disease": disease_info["disease"],
            "class_name": class_name,
            "confidence": confidence,
            "user_query": user_query,
            "symptoms": disease_info["symptoms"],
            "causes": disease_info["causes"],
            "environment": disease_info["environment"],
            "treatment": disease_info["treatment"],
            "prevention": disease_info["prevention"]
        }
    else:
        return {
            "detected": False,
            "user_query": user_query,
            "confidence": 0,
            "message": "Could not identify disease from your description. Please provide more details about symptoms."
        }

def generate_voice_response(disease_dict: Dict, language: str = "English") -> str:
    """
    Generate a detailed voice-friendly response about the detected disease.
    
    Args:
        disease_dict: Disease detection result
        language: Target language for response
    
    Returns:
        Formatted response text suitable for text-to-speech
    """
    if not disease_dict.get("detected"):
        response = disease_dict.get("message", "Could not identify the disease.")
        if language != "English":
            response = translate_text(response, language)
        return response
    
    leaf_type = disease_dict.get("leaf_type", "")
    disease = disease_dict.get("disease", "")
    confidence = disease_dict.get("confidence", 0)
    symptoms = disease_dict.get("symptoms", [])
    treatment = disease_dict.get("treatment", [])
    
    # Build response
    response = f"I detected a {leaf_type} leaf with possible {disease} disease. "
    response += f"Confidence level: {int(confidence * 100)}%. "
    
    # Add symptoms
    if symptoms:
        response += f"The symptoms I found are: {', '.join(symptoms[:3])}. "
    
    # Add treatment recommendations
    if treatment:
        response += "Here are the recommended treatments: "
        for i, treatment_step in enumerate(treatment[:3], 1):
            response += f"{i}. {treatment_step}. "
    
    response += "Please consult with a local agricultural expert for confirmation and personalized advice."
    
    # Translate if needed
    if language != "English":
        response = translate_text(response, language)
    
    return response

def process_voice_symptom_description(description: str, language: str = "English") -> Dict:
    """
    Process a voice description of symptoms and provide disease information.
    
    Args:
        description: Symptom description from user
        language: Language of input
    
    Returns:
        Dict with disease detection and treatment info
    """
    # First detect disease from description
    detection = detect_leaf_and_disease_from_voice(description)
    
    # Generate appropriate response
    response = generate_voice_response(detection, language)
    
    return {
        "detection": detection,
        "response": response,
        "language": language,
        "user_description": description
    }

def validate_voice_input(transcribed_text: str) -> Tuple[bool, str]:
    """
    Validate if voice input is suitable for disease detection.
    
    Args:
        transcribed_text: Text from speech-to-text
    
    Returns:
        Tuple of (is_valid, validation_message)
    """
    if not transcribed_text or len(transcribed_text.strip()) < 5:
        return False, "Please provide more details about the symptoms."
    
    # Check for disease-related keywords
    disease_keywords = [
        "disease", "blight", "rust", "scab", "spot", "rot", "mold",
        "symptom", "leaf", "plant", "crop", "sick", "infected",
        "fungal", "bacterial", "virus", "treatment", "cure"
    ]
    
    has_disease_keyword = any(keyword in transcribed_text.lower() for keyword in disease_keywords)
    
    if not has_disease_keyword:
        return True, "Please describe symptoms if you want disease identification."
    
    return True, "Valid"

def get_leaf_type_info(leaf_type: str) -> Dict:
    """
    Get general information about a leaf type.
    
    Args:
        leaf_type: Name of the leaf type (e.g., "Tomato", "Potato")
    
    Returns:
        Dict with leaf type information
    """
    leaf_diseases = {}
    for class_name, info in DISEASE_SYMPTOMS_DB.items():
        if info["leaf_type"] == leaf_type:
            leaf_diseases[info["disease"]] = {
                "symptoms": info["symptoms"],
                "treatment": info["treatment"]
            }
    
    return {
        "leaf_type": leaf_type,
        "common_diseases": leaf_diseases,
        "total_diseases": len(leaf_diseases)
    }
