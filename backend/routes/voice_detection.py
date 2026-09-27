"""
Enhanced Voice-Based Disease Detection Routes
Handles voice input for symptom description and disease identification
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import traceback

from backend.services.voice_disease_assistant import (
    detect_leaf_and_disease_from_voice,
    process_voice_symptom_description,
    validate_voice_input,
    generate_voice_response,
    get_leaf_type_info
)
from backend.services.text_to_speech_service import prepare_tts_output

router = APIRouter(prefix="/api/voice", tags=["voice-disease-detection"])

# ============ Request Models ============

class VoiceSymptomRequest(BaseModel):
    """Request model for voice symptom description"""
    transcribed_text: str
    language: Optional[str] = "English"
    confidence: Optional[float] = 0.95

class VoiceDetectionRequest(BaseModel):
    """Request model for disease detection from voice"""
    description: str
    language: Optional[str] = "English"

class LeafTypeRequest(BaseModel):
    """Request model for getting leaf type information"""
    leaf_type: str

# ============ Voice Disease Detection Routes ============

@router.post("/detect-from-symptoms")
async def detect_disease_from_voice_symptoms(request: VoiceSymptomRequest):
    """
    Detect disease from voice-transcribed symptom description.
    
    **Request Body:**
    - transcribed_text: Text transcribed from user voice
    - language: Language of the input (optional, defaults to English)
    - confidence: Confidence of transcription (optional)
    
    **Response:**
    - detected: Whether disease was detected
    - leaf_type: Type of leaf detected
    - disease: Disease name
    - confidence: Confidence of detection
    - symptoms: List of symptoms
    - treatment: List of treatments
    - response: Voice-friendly response
    """
    try:
        # Validate input
        is_valid, message = validate_voice_input(request.transcribed_text)
        
        if not is_valid:
            return {
                "success": True,
                "detected": False,
                "message": message,
                "transcribed_text": request.transcribed_text,
                "language": request.language
            }
        
        # Process symptom description
        result = process_voice_symptom_description(
            request.transcribed_text,
            request.language
        )
        
        detection = result["detection"]
        
        # ⚠️ CONFIDENCE CHECK - Reject low-confidence detections
        confidence = detection.get("confidence", 0)
        if detection.get("detected") and confidence < 0.35:
            return {
                "success": True,
                "detected": False,
                "message": "Could not confidently identify disease from voice input. Please describe symptoms more clearly or use image upload instead.",
                "transcribed_text": request.transcribed_text,
                "language": request.language,
                "debug_confidence": confidence  # For debugging purposes
            }
        
        return {
            "success": True,
            "detected": detection.get("detected", False),
            "leaf_type": detection.get("leaf_type"),
            "disease": detection.get("disease"),
            "confidence": detection.get("confidence", 0),
            "symptoms": detection.get("symptoms", []),
            "causes": detection.get("causes"),
            "environment": detection.get("environment"),
            "treatment": detection.get("treatment", []),
            "prevention": detection.get("prevention", []),
            "response": result["response"],
            "transcribed_text": request.transcribed_text,
            "language": request.language
        }
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Voice detection error: {str(e)}")


@router.post("/identify-leaf-disease")
async def identify_leaf_and_disease(request: VoiceDetectionRequest):
    """
    Identify leaf type and disease from user description.
    
    **Request Body:**
    - description: Description of the leaf/plant issue
    - language: Language of the input (optional)
    
    **Response:**
    - detected: Whether detected successfully
    - leaf_type: Type of leaf
    - disease: Disease name
    - class_name: Internal class name
    - confidence: Detection confidence (0-1)
    - symptoms: Associated symptoms
    - causes: Disease causes
    - treatment: Treatment recommendations
    - prevention: Prevention tips
    """
    try:
        detection = detect_leaf_and_disease_from_voice(request.description)
        
        if detection.get("detected"):
            # Generate voice-friendly response
            response_text = generate_voice_response(detection, request.language)
            
            return {
                "success": True,
                "detected": True,
                "leaf_type": detection.get("leaf_type"),
                "disease": detection.get("disease"),
                "class_name": detection.get("class_name"),
                "confidence": detection.get("confidence", 0),
                "symptoms": detection.get("symptoms", []),
                "causes": detection.get("causes"),
                "environment": detection.get("environment"),
                "treatment": detection.get("treatment", []),
                "prevention": detection.get("prevention", []),
                "voice_response": response_text,
                "tts_config": prepare_tts_output(response_text, 
                                                language_code="en-US" if request.language == "English" else "hi-IN")
            }
        else:
            error_message = detection.get("message", "Could not identify disease.")
            
            return {
                "success": True,
                "detected": False,
                "message": error_message,
                "suggestion": "Please describe the symptoms in more detail. For example, mention the color of spots, their pattern, or when they appeared.",
                "language": request.language
            }
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Disease identification error: {str(e)}")


@router.get("/leaf-types")
async def get_available_leaf_types():
    """
    Get all available leaf types in the disease database.
    
    **Response:**
    - leaf_types: List of available leaf types
    - total_types: Number of leaf types
    """
    try:
        from backend.services.voice_disease_assistant import DISEASE_SYMPTOMS_DB
        
        leaf_types = set()
        for class_name, info in DISEASE_SYMPTOMS_DB.items():
            leaf_types.add(info["leaf_type"])
        
        return {
            "success": True,
            "leaf_types": sorted(list(leaf_types)),
            "total_types": len(leaf_types)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting leaf types: {str(e)}")


@router.get("/leaf-info/{leaf_type}")
async def get_leaf_information(leaf_type: str):
    """
    Get detailed information about a specific leaf type and its diseases.
    
    **Path Parameters:**
    - leaf_type: Name of the leaf type (e.g., 'Tomato', 'Potato', 'Apple')
    
    **Response:**
    - leaf_type: The leaf type
    - common_diseases: Dictionary of diseases for this leaf type
    - total_diseases: Number of diseases for this leaf type
    """
    try:
        leaf_info = get_leaf_type_info(leaf_type)
        
        if leaf_info.get("total_diseases", 0) == 0:
            raise HTTPException(status_code=404, 
                              detail=f"No diseases found for leaf type: {leaf_type}")
        
        return {
            "success": True,
            "leaf_type": leaf_info["leaf_type"],
            "diseases": leaf_info["common_diseases"],
            "total_diseases": leaf_info["total_diseases"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting leaf info: {str(e)}")


@router.post("/validate-voice-input")
async def validate_voice_input_endpoint(request: VoiceSymptomRequest):
    """
    Validate voice transcription for disease detection.
    
    **Request Body:**
    - transcribed_text: Text from speech-to-text
    - language: Language (optional)
    
    **Response:**
    - is_valid: Whether input is valid
    - message: Validation message
    - suggestion: Suggestion if invalid
    """
    try:
        is_valid, message = validate_voice_input(request.transcribed_text)
        
        return {
            "success": True,
            "is_valid": is_valid,
            "message": message,
            "transcribed_text": request.transcribed_text,
            "suggestion": "Describe symptoms like color, pattern, location on leaf, and when they started." if not is_valid else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")


@router.get("/disease-keywords")
async def get_disease_keywords():
    """
    Get keywords that help identify disease-related voice input.
    
    **Response:**
    - keywords: List of disease-related keywords
    """
    try:
        keywords = [
            "disease", "blight", "rust", "scab", "spot", "rot", "mold",
            "symptom", "leaf", "plant", "crop", "sick", "infected",
            "fungal", "bacterial", "virus", "treatment", "cure",
            "brown", "yellow", "white", "black", "lesion", "ring"
        ]
        
        return {
            "success": True,
            "keywords": keywords,
            "total_keywords": len(keywords),
            "usage": "Use these keywords in voice descriptions for better disease detection"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
