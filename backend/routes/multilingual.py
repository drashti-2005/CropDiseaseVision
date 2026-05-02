"""
Multilingual Routes for Crop Disease Vision API
Handles translation, speech-to-text, text-to-speech, and chat features
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, Dict, List
import json
import traceback

from backend.services.translation_service import (
    translate_text,
    translate_disease_result,
    get_supported_languages as get_translation_languages
)
from backend.services.speech_to_text_service import (
    process_transcription,
    validate_audio_input,
    clean_transcription,
    get_supported_languages as get_stt_languages
)
from backend.services.text_to_speech_service import (
    prepare_tts_output,
    validate_tts_input,
    cleanup_text_for_speech,
    get_supported_languages as get_tts_languages
)
from backend.services.chat_assistant_service import (
    process_farmer_question,
    generate_greeting,
    get_supported_languages as get_chat_languages
)

router = APIRouter(prefix="/api/multilingual", tags=["multilingual"])

# ============ Request Models ============

class TranslationRequest(BaseModel):
    """Request model for translation"""
    text: str
    target_language: str
    source_language: Optional[str] = "English"

class DiseaseTranslationRequest(BaseModel):
    """Request model for disease result translation"""
    disease: str
    status: str
    description: str
    treatment: str
    confidence: float
    target_language: str

class TranscriptionRequest(BaseModel):
    """Request model for speech-to-text processing"""
    transcribed_text: str
    language_code: Optional[str] = "en-US"
    confidence: Optional[float] = 0.95

class TTSRequest(BaseModel):
    """Request model for text-to-speech"""
    text: str
    language_code: Optional[str] = "en-US"
    voice_name: Optional[str] = None

class ChatRequest(BaseModel):
    """Request model for chat assistant"""
    question: str
    language: Optional[str] = "English"
    context: Optional[Dict] = None

class LanguageListRequest(BaseModel):
    """Request model for getting supported languages"""
    service: Optional[str] = None  # 'translation', 'stt', 'tts', 'chat'

# ============ Translation APIs ============

@router.post("/translate")
async def translate_text_endpoint(request: TranslationRequest):
    """
    Translate text to target language.
    
    **Request Body:**
    - text: Text to translate
    - target_language: Target language name (e.g., 'Gujarati')
    - source_language: Source language (optional, defaults to English)
    
    **Response:**
    - translated_text: Translated text
    - source_language: Source language used
    - target_language: Target language
    - status: Success or error status
    """
    try:
        if not request.text or len(request.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        translated = translate_text(request.text, request.target_language)
        
        return {
            "success": True,
            "original_text": request.text,
            "translated_text": translated,
            "source_language": request.source_language,
            "target_language": request.target_language,
            "status": "completed"
        }
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")


@router.post("/translate-disease")
async def translate_disease_endpoint(request: DiseaseTranslationRequest):
    """
    Translate disease detection result to target language.
    
    **Request Body:**
    - disease: Disease name
    - status: Disease status ('Healthy' or 'Diseased')
    - description: Disease description
    - treatment: Treatment recommendation
    - confidence: Confidence score
    - target_language: Target language
    
    **Response:**
    - Translated disease result with all fields
    """
    try:
        result_dict = {
            "disease": request.disease,
            "status": request.status,
            "description": request.description,
            "treatment": request.treatment,
            "confidence": request.confidence
        }
        
        translated_result = translate_disease_result(result_dict, request.target_language)
        
        return {
            "success": True,
            "original": result_dict,
            "translated": translated_result,
            "status": "completed"
        }
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")


# ============ Speech-to-Text APIs ============

@router.post("/speech-to-text")
async def speech_to_text_endpoint(request: TranscriptionRequest):
    """
    Process transcribed speech to text.
    
    **Request Body:**
    - transcribed_text: Text from Web Speech API or STT service
    - language_code: Language code (e.g., 'gu-IN', 'hi-IN')
    - confidence: Confidence score from speech recognition
    
    **Response:**
    - Processed transcription with language detection and cleaning
    """
    try:
        if not request.transcribed_text or len(request.transcribed_text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Transcribed text cannot be empty")
        
        # Clean the transcription
        cleaned_text = clean_transcription(request.transcribed_text)
        
        # Process and validate
        result = process_transcription(
            cleaned_text,
            request.language_code,
            request.confidence
        )
        
        return {
            "success": result['success'],
            "transcribed_text": result.get('transcribed_text'),
            "language_code": result.get('language_code'),
            "language_name": result.get('language_name'),
            "confidence": result.get('confidence'),
            "status": result.get('status')
        }
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"STT processing error: {str(e)}")


@router.post("/speech-to-text/upload")
async def speech_to_text_upload(
    file: UploadFile = File(...),
    language_code: Optional[str] = "en-US"
):
    """
    Process uploaded audio file (placeholder for future integration).
    
    **Note:** Frontend currently uses Web Speech API.
    This endpoint is for future backend audio processing.
    """
    try:
        contents = await file.read()
        
        # Validate audio
        is_valid = validate_audio_input(contents)
        if not is_valid:
            raise HTTPException(status_code=400, detail="Invalid audio file format")
        
        return {
            "success": True,
            "message": "Audio received. Currently using Web Speech API for transcription.",
            "file_size": len(contents),
            "language_code": language_code
        }
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Audio upload error: {str(e)}")


# ============ Text-to-Speech APIs ============

@router.post("/text-to-speech")
async def text_to_speech_endpoint(request: TTSRequest):
    """
    Prepare text for speech synthesis.
    
    **Request Body:**
    - text: Text to convert to speech
    - language_code: Language code (e.g., 'gu-IN', 'en-US')
    - voice_name: Optional specific voice
    
    **Response:**
    - TTS configuration ready for frontend Web Speech API
    """
    try:
        # Validate input
        validation = validate_tts_input(request.text, request.language_code)
        if not validation['valid']:
            raise HTTPException(status_code=400, detail=f"Validation error: {validation['errors']}")
        
        # Clean text for better speech
        cleaned_text = cleanup_text_for_speech(request.text)
        
        # Prepare TTS output
        tts_config = prepare_tts_output(cleaned_text, request.language_code, request.voice_name)
        
        return {
            "success": True,
            "text": cleaned_text,
            "language_code": request.language_code,
            "voice_name": tts_config['voice_name'],
            "audio_config": tts_config['audio_config'],
            "method": "web_speech_api",
            "status": "ready_for_playback"
        }
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")


# ============ Chat Assistant APIs ============

@router.post("/chat")
async def chat_assistant_endpoint(request: ChatRequest):
    """
    Process farmer question and generate response.
    
    **Request Body:**
    - question: Farmer's question
    - language: Language of response (e.g., 'Gujarati')
    - context: Optional context (e.g., detected disease)
    
    **Response:**
    - Assistant response in requested language
    """
    try:
        if not request.question or len(request.question.strip()) == 0:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        response = process_farmer_question(
            request.question,
            request.language,
            request.context
        )
        
        return {
            "success": True,
            "question": request.question,
            "response": response['response'],
            "language": response.get('language'),
            "category": response.get('category'),
            "confidence": response.get('confidence'),
            "status": "completed"
        }
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@router.get("/chat/greeting/{language}")
async def get_greeting(language: str = "English"):
    """
    Get greeting message for specific language.
    
    **Parameters:**
    - language: Language name (e.g., 'Gujarati')
    
    **Response:**
    - Greeting message in requested language
    """
    try:
        greeting = generate_greeting(language)
        
        return {
            "success": True,
            "greeting": greeting,
            "language": language
        }
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Greeting error: {str(e)}")


# ============ Utility APIs ============

@router.get("/languages")
async def get_supported_languages(service: Optional[str] = None):
    """
    Get list of supported languages.
    
    **Query Parameters:**
    - service: Service type ('translation', 'stt', 'tts', 'chat', or None for all)
    
    **Response:**
    - Dict of supported languages for requested service(s)
    """
    try:
        languages = {}
        
        if not service or service == 'translation':
            languages['translation'] = get_translation_languages()
        
        if not service or service == 'stt':
            languages['speech_to_text'] = get_stt_languages()
        
        if not service or service == 'tts':
            languages['text_to_speech'] = get_tts_languages()
        
        if not service or service == 'chat':
            languages['chat'] = get_chat_languages()
        
        return {
            "success": True,
            "languages": languages,
            "status": "completed"
        }
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Language retrieval error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint for multilingual services."""
    return {
        "status": "healthy",
        "service": "multilingual",
        "services": [
            "translation",
            "speech-to-text",
            "text-to-speech",
            "chat-assistant"
        ]
    }
