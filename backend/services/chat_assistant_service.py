"""
Farmer Chat Assistant Service
Provides multilingual support for farmer questions about diseases, treatments, etc.
"""

from typing import Optional, Dict, List
import json

# Knowledge base for farmer questions
FARMER_KNOWLEDGE_BASE = {
    'disease_info': {
        'What are the symptoms?': {
            'keywords': ['symptoms', 'signs', 'how to know', 'identify'],
            'response_template': 'The disease shows: {symptoms}'
        },
        'How to treat?': {
            'keywords': ['treatment', 'cure', 'fix', 'remedy', 'medicine'],
            'response_template': 'Treatment: {treatment}'
        },
        'How to prevent?': {
            'keywords': ['prevent', 'prevention', 'avoid', 'protect', 'precaution'],
            'response_template': 'Prevention: {prevention}'
        },
        'Why did this happen?': {
            'keywords': ['why', 'cause', 'reason', 'caused'],
            'response_template': 'This disease occurs due to: {causes}'
        }
    },
    'general_farming': {
        'crop_rotation': {
            'keywords': ['crop rotation', 'rotate crops', 'what to plant next'],
            'response': 'Practice crop rotation by planting different crops in the same field each season to reduce disease buildup.'
        },
        'watering': {
            'keywords': ['watering', 'water', 'irrigation', 'how much water'],
            'response': 'Water your crops regularly, preferably in the morning at the base of plants to prevent fungal diseases.'
        },
        'fertilizer': {
            'keywords': ['fertilizer', 'manure', 'nutrients', 'soil'],
            'response': 'Use organic manure and balanced fertilizers to maintain soil health and plant immunity.'
        },
        'pest_management': {
            'keywords': ['pest', 'insect', 'bug', 'worm'],
            'response': 'Use integrated pest management including organic methods, beneficial insects, and targeted pesticides if needed.'
        }
    }
}

# Multilingual responses
MULTILINGUAL_RESPONSES = {
    'Gujarati': {
        'greeting': 'નમસ્તે! હું તમારો પાક સ્વાસ્થ્ય સહાયક છું. તમને શું મદદ ચાહીએ?',
        'help': 'હું તમને રોગ વિશે, સારવાર વિશે અને નિવારણ વિશે મદદ કરી શકું છું.',
        'unknown': 'મને માફ કરો, મને તમારો પ્રશ્ન સમજાયો નહીં. કૃપા કરીને ફરીથી પુછો.',
        'need_expert': 'આ જટિલ સમસ્યા છે. કૃપા કરીને સ્થાનિક કૃષિ વિશેષજ્ञને સલાહ કરો.'
    },
    'Hindi': {
        'greeting': 'नमस्ते! मैं आपका फसल स्वास्थ्य सहायक हूँ। आपको क्या सहायता चाहिए?',
        'help': 'मैं आपको रोग, उपचार और रोकथाम के बारे में मदद कर सकता हूँ।',
        'unknown': 'मुझे खेद है, मुझे आपका सवाल समझ नहीं आया। कृपया फिर से पूछें।',
        'need_expert': 'यह एक जटिल समस्या है। कृपया स्थानीय कृषि विशेषज्ञ से सलाह लें।'
    },
    'English': {
        'greeting': 'Hello! I am your crop health assistant. How can I help you?',
        'help': 'I can help you with disease information, treatments, and prevention tips.',
        'unknown': 'Sorry, I did not understand your question. Please ask again.',
        'need_expert': 'This is a complex issue. Please consult a local agricultural expert.'
    },
    'Marathi': {
        'greeting': 'नमस्कार! मी तुमचा पिक स्वास्थ्य सहायक आहे. मी तुम्हाला कसे मदत करू शकतो?',
        'help': 'मी तुम्हाला रोग, उपचार आणि प्रतिबंध बद्दल मदत करू शकतो.',
        'unknown': 'मला खेद आहे, मला तुमचा प्रश्न समजला नाही. कृपया पुन्हा विचारा.',
        'need_expert': 'हा एक जटिल मुद्दा आहे. कृपया स्थानिक कृषी तज्ञाचा सल्ला घ्या.'
    },
    'Tamil': {
        'greeting': 'வணக்கம்! நான் உங்கள் பயிர் சுகாதாร உதவியாளர். நான் உங்களுக்கு எப்படி உதவ முடியும்?',
        'help': 'நோய், சிகிச்சை மற்றும் தடுப்பு பற்றி உங்களுக்கு உதவ முடியும்.',
        'unknown': 'மன்னிக்கவும், உங்கள் கேள்வியை நான் புரிந்துகொள்ளவில்லை. மீண்டும் கேளுங்கள்.',
        'need_expert': 'இது ஒரு சிக்கலான பிரச்சினை. உள்ளூர் விவசாய நிபுணரிடம் ஆலோசனை பெறவும்.'
    },
    'Telugu': {
        'greeting': 'హలో! నేను మీ పంట ఆరోగ్య సహాయకుడిని. నేను మీకు ఎలా సహాయం చేయగలను?',
        'help': 'నేను మీకు వ్యాధి, చికిత్స మరియు నిరోధం గురించి సహాయం చేయగలను.',
        'unknown': 'క్షమించండి, నేను మీ ప్రశ్నను అర్థం చేసుకోలేదు. దయచేసి మళ్ళీ అడగండి.',
        'need_expert': 'ఇది ఒక సంక్లిష్ట సమస్య. దయచేసి స్థానిక వ్యవసాయ నిపుణుడిని సంప్రదించండి.'
    }
}

# Farmer-friendly disease information
DISEASE_FAQ = {
    'Apple___Apple_scab': {
        'symptoms': 'Dark, scabby spots on leaves and fruit',
        'causes': 'Fungal infection in wet, cool weather',
        'treatment': 'Remove fallen leaves, apply fungicide',
        'prevention': 'Prune tree for air circulation, remove infected parts'
    },
    'Potato___Early_blight': {
        'symptoms': 'Brown spots with concentric rings on lower leaves',
        'causes': 'Fungal spores spread by water and wind',
        'treatment': 'Remove infected leaves, apply fungicide early',
        'prevention': 'Ensure good spacing, avoid overhead watering'
    },
    'Tomato___Early_blight': {
        'symptoms': 'Target-like spots starting from bottom leaves',
        'causes': 'Fungal infection in humid conditions',
        'treatment': 'Remove lower leaves, apply fungicide',
        'prevention': 'Mulch around plants, water at base only'
    },
    'default': {
        'symptoms': 'Visible damage to crop',
        'causes': 'Various environmental and pathogenic factors',
        'treatment': 'Consult local agricultural expert',
        'prevention': 'Practice good crop management'
    }
}


def generate_greeting(language: str = 'English') -> str:
    """
    Generate greeting message in farmer's language.
    
    Args:
        language: Language name (e.g., 'Gujarati')
    
    Returns:
        Greeting message
    """
    responses = MULTILINGUAL_RESPONSES.get(language, MULTILINGUAL_RESPONSES['English'])
    return responses['greeting']


def process_farmer_question(question: str, language: str = 'English', context: Optional[Dict] = None) -> Dict:
    """
    Process farmer's question and generate response.
    
    Args:
        question: Farmer's question
        language: Language of question
        context: Additional context (e.g., disease detected)
    
    Returns:
        Dict with response and metadata
    """
    try:
        # Get language responses
        lang_responses = MULTILINGUAL_RESPONSES.get(language, MULTILINGUAL_RESPONSES['English'])
        
        if not question or len(question.strip()) == 0:
            return {
                'response': lang_responses['help'],
                'confidence': 0.95,
                'category': 'help',
                'language': language
            }
        
        # Normalize question
        question_lower = question.lower().strip()
        
        # Check for disease-specific questions if context provided
        if context and 'disease' in context:
            disease_info = DISEASE_FAQ.get(context['disease'], DISEASE_FAQ['default'])
            
            if any(keyword in question_lower for keyword in ['symptom', 'sign', 'look like']):
                return {
                    'response': f'Symptoms: {disease_info["symptoms"]}',
                    'confidence': 0.9,
                    'category': 'symptoms',
                    'language': language
                }
            
            if any(keyword in question_lower for keyword in ['treat', 'cure', 'fix', 'medicine']):
                return {
                    'response': f'Treatment: {disease_info["treatment"]}',
                    'confidence': 0.9,
                    'category': 'treatment',
                    'language': language
                }
            
            if any(keyword in question_lower for keyword in ['prevent', 'avoid', 'protection']):
                return {
                    'response': f'Prevention: {disease_info["prevention"]}',
                    'confidence': 0.9,
                    'category': 'prevention',
                    'language': language
                }
        
        # General farming advice
        if any(keyword in question_lower for keyword in ['watering', 'water', 'irrigation']):
            response = FARMER_KNOWLEDGE_BASE['general_farming']['watering']['response']
        elif any(keyword in question_lower for keyword in ['fertilizer', 'manure', 'nutrients']):
            response = FARMER_KNOWLEDGE_BASE['general_farming']['fertilizer']['response']
        elif any(keyword in question_lower for keyword in ['pest', 'insect', 'bug']):
            response = FARMER_KNOWLEDGE_BASE['general_farming']['pest_management']['response']
        elif any(keyword in question_lower for keyword in ['rotation', 'crop rotation']):
            response = FARMER_KNOWLEDGE_BASE['general_farming']['crop_rotation']['response']
        else:
            response = lang_responses['unknown']
        
        return {
            'response': response,
            'confidence': 0.7,
            'category': 'general',
            'language': language
        }
        
    except Exception as e:
        print(f"Error processing question: {e}")
        lang_responses = MULTILINGUAL_RESPONSES.get(language, MULTILINGUAL_RESPONSES['English'])
        return {
            'response': lang_responses['unknown'],
            'confidence': 0.0,
            'category': 'error',
            'language': language,
            'error': str(e)
        }


def format_response_for_display(response: Dict, max_length: int = 500) -> str:
    """
    Format assistant response for display.
    
    Args:
        response: Response dict from assistant
        max_length: Maximum character length
    
    Returns:
        Formatted response string
    """
    text = response.get('response', '')
    
    if len(text) > max_length:
        text = text[:max_length] + '...'
    
    return text


def get_supported_languages() -> Dict[str, str]:
    """
    Get supported languages for chat assistant.
    
    Returns:
        Dict of language codes and names
    """
    return {
        'en': 'English',
        'gu': 'Gujarati',
        'hi': 'Hindi',
        'mr': 'Marathi',
        'ta': 'Tamil',
        'te': 'Telugu'
    }


def create_system_prompt(language: str = 'English') -> str:
    """
    Create system prompt for chat assistant in farmer's language.
    
    Args:
        language: Language name
    
    Returns:
        System prompt
    """
    prompts = {
        'English': 'You are a helpful agricultural assistant for farmers. Provide simple, practical advice about crop diseases, treatments, and prevention. Keep responses short and easy to understand.',
        'Gujarati': 'તમે ખેડૂતો માટે મદદરૂપ કૃષિ સહાયક છો. પાક રોગ, સારવાર અને નિવારણ વિશે સરળ, વ્યવહારિક સલાહ આપો.',
        'Hindi': 'आप किसानों के लिए एक सहायक कृषि सहायक हैं। फसल रोग, उपचार और रोकथाम के बारे में सरल, व्यावहारिक सलाह दें।',
        'Marathi': 'तुम शेतकरीमाठे एक मदतनीस कृषि सहायक आहात. पिक रोग, उपचार व प्रतिबंध बद्दल सोपे, व्यावहारिक सल्ले द्या.',
        'Tamil': 'நீங்கள் விவசாயிகளுக்கான உதவிகரமான விவசாய உதவியாளர். பயிர் நோய், சிகிच்சை மற்றும் தடுப்பு பற்றி எளிய, நடைமுறை ஆலோசனை வழங்கவும்.',
        'Telugu': 'మీరు రైతుల కోసం ఉపయోగకరమైన స农业 సహాయకుడిని. పంట వ్యాధి, చికిత్స మరియు నిరోధం గురించి సరళ, ఆచరణాత్మక సలహా ఇవ్వండి.'
    }
    return prompts.get(language, prompts['English'])
