"""
Speech-to-Text Service
Converts audio to text with language detection
Supports multilingual transcription
"""

from typing import Optional, Dict, Tuple
import os
import json

# Language codes mapping
LANGUAGE_CODES = {
    'gujarati': 'gu-IN',
    'hindi': 'hi-IN',
    'english': 'en-US',
    'marathi': 'mr-IN',
    'tamil': 'ta-IN',
    'telugu': 'te-IN'
}

LANGUAGE_NAMES = {
    'gu-IN': 'Gujarati',
    'hi-IN': 'Hindi',
    'en-US': 'English',
    'mr-IN': 'Marathi',
    'ta-IN': 'Tamil',
    'te-IN': 'Telugu'
}


def transcribe_audio_web_speech(audio_blob: bytes, language_code: str = 'en-US') -> Optional[str]:
    """
    Handle Web Speech API transcription from frontend.
    This receives the transcribed text from frontend Web Speech API.
    
    Args:
        audio_blob: Raw audio data (unused - frontend does transcription)
        language_code: Language code for transcription
    
    Returns:
        Transcribed text
    """
    # Note: Web Speech API transcription happens on frontend
    # This function is for reference/future backend processing
    return None


def validate_audio_input(file_data: bytes, expected_format: str = 'wav') -> bool:
    """
    Validate audio input format.
    
    Args:
        file_data: Audio file bytes
        expected_format: Expected file format
    
    Returns:
        True if valid, False otherwise
    """
    try:
        # Check file size (max 25MB for most APIs)
        if len(file_data) > 25 * 1024 * 1024:
            return False
        
        # Check audio format headers
        if expected_format == 'wav':
            # WAV files start with RIFF header
            return file_data[:4] == b'RIFF' and file_data[8:12] == b'WAVE'
        elif expected_format == 'mp3':
            # MP3 files can start with ID3 or FF
            return file_data[:2] == b'ID' or file_data[0:1] == b'\xff'
        elif expected_format == 'webm':
            # WEBM files start with 1A 45 DF A3
            return file_data[:4] == b'\x1a\x45\xdf\xa3'
        
        return True  # Default to True if format not specified
        
    except Exception as e:
        print(f"Audio validation error: {e}")
        return False


def detect_language(text: str) -> Tuple[Optional[str], float]:
    """
    Detect language of transcribed text.
    
    Args:
        text: Transcribed text
    
    Returns:
        Tuple of (language_code, confidence)
    """
    try:
        from textblob import TextBlob
        blob = TextBlob(text)
        language_code = blob.detect_language()
        
        # Map language codes
        language_map = {
            'en': 'en-US',
            'gu': 'gu-IN',
            'hi': 'hi-IN',
            'mr': 'mr-IN',
            'ta': 'ta-IN',
            'te': 'te-IN'
        }
        
        return language_map.get(language_code, 'en-US'), 0.85
        
    except Exception as e:
        print(f"Language detection error: {e}")
        return 'en-US', 0.5


def process_transcription(
    transcribed_text: str,
    language_code: str = 'en-US',
    confidence: float = 0.95
) -> Dict:
    """
    Process transcribed text and return structured data.
    
    Args:
        transcribed_text: Transcribed text from speech-to-text
        language_code: Language code
        confidence: Confidence score from speech recognition
    
    Returns:
        Structured transcription result
    """
    try:
        # Detect language if not provided
        if not language_code or language_code == 'auto':
            detected_lang, detection_confidence = detect_language(transcribed_text)
            language_code = detected_lang
            confidence = detection_confidence
        
        language_name = LANGUAGE_NAMES.get(language_code, 'Unknown')
        
        return {
            'success': True,
            'text': transcribed_text,
            'transcribed_text': transcribed_text,
            'language_code': language_code,
            'language_name': language_name,
            'confidence': confidence,
            'status': 'completed'
        }
        
    except Exception as e:
        print(f"Transcription processing error: {e}")
        return {
            'success': False,
            'error': str(e),
            'status': 'failed'
        }


def clean_transcription(text: str) -> str:
    """
    Clean up transcribed text (remove extra spaces, fix punctuation, etc).
    
    Args:
        text: Raw transcribed text
    
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Add period if missing
    if text and not text.endswith(('.', '?', '!')):
        text += '.'
    
    return text


def get_supported_languages() -> Dict[str, str]:
    """
    Get list of supported languages for speech-to-text.
    
    Returns:
        Dict of language codes and names
    """
    return {
        'en-US': 'English',
        'gu-IN': 'Gujarati',
        'hi-IN': 'Hindi',
        'mr-IN': 'Marathi',
        'ta-IN': 'Tamil',
        'te-IN': 'Telugu'
    }


def get_language_code(language_name: str) -> Optional[str]:
    """
    Get language code from language name.
    
    Args:
        language_name: Language name (e.g., 'Gujarati')
    
    Returns:
        Language code (e.g., 'gu-IN') or None
    """
    return LANGUAGE_CODES.get(language_name.lower())
