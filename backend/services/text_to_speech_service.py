"""
Text-to-Speech Service
Converts text to audio with multilingual support
"""

from typing import Optional, Dict
import os
import base64

# Language codes for TTS
LANGUAGE_CODES = {
    'gujarati': 'gu-IN',
    'hindi': 'hi-IN',
    'english': 'en-US',
    'marathi': 'mr-IN',
    'tamil': 'ta-IN',
    'telugu': 'te-IN'
}

SUPPORTED_VOICES = {
    'en-US': ['en-US-Neural2-A', 'en-US-Neural2-C'],
    'gu-IN': ['gu-IN-Standard-A', 'gu-IN-Standard-B'],
    'hi-IN': ['hi-IN-Standard-A', 'hi-IN-Standard-B'],
    'mr-IN': ['mr-IN-Standard-A', 'mr-IN-Standard-B'],
    'ta-IN': ['ta-IN-Standard-A', 'ta-IN-Standard-B'],
    'te-IN': ['te-IN-Standard-A', 'te-IN-Standard-B']
}


def synthesize_speech_web(text: str, language_code: str = 'en-US') -> Dict:
    """
    Use Web Speech Synthesis API info for frontend.
    Frontend will use Web Speech API SpeechSynthesis for actual audio generation.
    
    Args:
        text: Text to convert to speech
        language_code: Language code (e.g., 'gu-IN')
    
    Returns:
        Dict with synthesis info for frontend
    """
    return {
        'text': text,
        'language_code': language_code,
        'method': 'web_speech_api',
        'ready_for_playback': True,
        'voice_options': SUPPORTED_VOICES.get(language_code, [])
    }


def prepare_tts_output(
    text: str,
    language_code: str = 'en-US',
    voice_name: Optional[str] = None
) -> Dict:
    """
    Prepare text-to-speech output.
    
    Args:
        text: Text to synthesize
        language_code: Language code
        voice_name: Specific voice name
    
    Returns:
        TTS configuration dict
    """
    # Get default voice if not specified
    if not voice_name:
        available_voices = SUPPORTED_VOICES.get(language_code, ['default'])
        voice_name = available_voices[0] if available_voices else 'default'
    
    return {
        'text': text,
        'language': language_code,
        'language_code': language_code,
        'voice_name': voice_name,
        'audio_config': {
            'audio_encoding': 'MP3',
            'speaking_rate': 1.0,
            'pitch': 0.0
        },
        'method': 'web_speech_api'
    }


def validate_tts_input(text: str, language_code: str) -> bool:
    """
    Validate text-to-speech input.
    
    Args:
        text: Text to validate
        language_code: Language code to validate
    
    Returns:
        True if valid, False otherwise
    """
    # Check text
    if not text or len(text.strip()) == 0:
        return False
    
    if len(text) > 5000:
        return False
    
    # Check language code
    if language_code not in SUPPORTED_VOICES:
        return False
    
    return True


def cleanup_text_for_speech(text: str) -> str:
    """
    Clean up text for better speech synthesis.
    
    Args:
        text: Raw text
    
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Replace common symbols
    replacements = {
        '&': 'and',
        '@': 'at',
        '#': 'number',
        '$': 'dollar',
        '%': 'percent'
    }
    
    for symbol, replacement in replacements.items():
        text = text.replace(symbol, replacement)
    
    return text


def get_supported_languages() -> Dict[str, str]:
    """
    Get list of supported languages for text-to-speech.
    
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


def get_voices_for_language(language_code: str) -> list:
    """
    Get available voices for a language.
    
    Args:
        language_code: Language code
    
    Returns:
        List of voice names
    """
    return SUPPORTED_VOICES.get(language_code, [])
