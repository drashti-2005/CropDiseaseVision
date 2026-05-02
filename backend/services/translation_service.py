"""
Translation Service for multilingual support
Supports: Gujarati, Hindi, English, Marathi, Tamil, Telugu
"""

from typing import Dict, Optional
import os

# Language codes mapping
LANGUAGE_CODES = {
    'gujarati': 'gu',
    'hindi': 'hi',
    'english': 'en',
    'marathi': 'mr',
    'tamil': 'ta',
    'telugu': 'te'
}

SUPPORTED_LANGUAGES = {
    'gu': 'Gujarati',
    'hi': 'Hindi',
    'en': 'English',
    'mr': 'Marathi',
    'ta': 'Tamil',
    'te': 'Telugu'
}

# Fallback translations for common disease terms
DISEASE_TRANSLATIONS = {
    'Gujarati': {
        'Apple scab': 'સફરજનના ખોલ',
        'Black rot': 'કાળો સ腐',
        'Cedar apple rust': 'દેવદારનો જંગ',
        'Powdery mildew': 'પાવડર જેવો ફૂલ',
        'Cercospora leaf spot': 'પર્ણ બિંદુ',
        'Common rust': 'સામાન્ય જંગ',
        'Northern Leaf Blight': 'ઉત્તરીય પર્ણ ધ્વજ',
        'Esca Black Measles': 'કાળો માપ',
        'Bacterial spot': 'બેક્ટેરિયલ સ્પોટ',
        'Early blight': 'શરૂઆતી ધ્વજ',
        'Late blight': 'મોડું ધ્વજ',
        'Leaf scorch': 'પર્ણ દાહ',
        'Leaf Mold': 'પર્ણ મોલ્ડ',
        'Septoria leaf spot': 'સેપ્ટોરિયા પર્ણ સ્પોટ',
        'Spider mites': 'કરોળી કણ',
        'Target Spot': 'લક્ષ્ય સ્પોટ',
        'Tomato mosaic virus': 'ટમેટો મોઝેક વાયરસ',
        'Tomato Yellow Leaf Curl Virus': 'ટમેટો પીળો પર્ણ કર્લ વાયરસ',
        'healthy': 'સુસ્થ',
        'Diseased': 'રોગી',
        'No treatment required': 'કોઈ સારવાર આवશ્યક નથી',
        'Maintain regular watering': 'નિયમિત પાણી આપવું જાળવો',
        'Disease detected': 'રોગ પહેલાચાણાયું',
        'Solution': 'સમાધાન',
        'Prevention': 'નિવારણ',
        'Symptoms': 'લક્ષણો',
        'Recommendation': 'ભલામણ',
        'Treatment': 'સારવાર'
    },
    'Hindi': {
        'Apple scab': 'सेब पपड़ी',
        'Black rot': 'काला सड़न',
        'Cedar apple rust': 'देवदार सेब जंग',
        'Powdery mildew': 'पाउडर फफूंदी',
        'Cercospora leaf spot': 'सर्कोस्पोरा पत्ती धब्बा',
        'Common rust': 'सामान्य जंग',
        'Northern Leaf Blight': 'उत्तरी पत्ती ब्लाइट',
        'Esca Black Measles': 'एस्का काली खसरा',
        'Bacterial spot': 'जीवाणु धब्बा',
        'Early blight': 'जल्दी झुलसा',
        'Late blight': 'देर से झुलसा',
        'Leaf scorch': 'पत्ती जलना',
        'Leaf Mold': 'पत्ती सड़न',
        'Septoria leaf spot': 'सेप्टोरिया पत्ती धब्बा',
        'Spider mites': 'मकड़ी के कण',
        'Target Spot': 'लक्ष्य धब्बा',
        'Tomato mosaic virus': 'टमाटर मोजेक वायरस',
        'Tomato Yellow Leaf Curl Virus': 'टमाटर पीला पत्ती कर्ल वायरस',
        'healthy': 'स्वस्थ',
        'Diseased': 'रोगी',
        'No treatment required': 'कोई उपचार की आवश्यकता नहीं',
        'Maintain regular watering': 'नियमित सिंचाई बनाए रखें',
        'Disease detected': 'रोग का पता चला',
        'Solution': 'समाधान',
        'Prevention': 'रोकथाम',
        'Symptoms': 'लक्षण',
        'Recommendation': 'सिफारिश',
        'Treatment': 'उपचार'
    },
    'Marathi': {
        'Apple scab': 'सेबांचा पपकळ',
        'Black rot': 'काळ्या गुदामांचा रोग',
        'Cedar apple rust': 'व्यधी ',
        'Powdery mildew': 'पाउडर फुगणे',
        'Cercospora leaf spot': 'पान डाग',
        'Common rust': 'सामान्य व्यधी',
        'Northern Leaf Blight': 'उत्तरीय पान ब्लाइट',
        'Esca Black Measles': 'काळा मसुरा',
        'Bacterial spot': 'जिवाणु डाग',
        'Early blight': 'लवकरातलवकर उजळणे',
        'Late blight': 'उशिरा उजळणे',
        'Leaf scorch': 'पान जाळणे',
        'Leaf Mold': 'पान साचूळ',
        'Septoria leaf spot': 'सेप्टोरिया पान डाग',
        'Spider mites': 'कोळी कण',
        'Target Spot': 'लक्ष्य डाग',
        'Tomato mosaic virus': 'टोमॅटोचा मोजेक व्हायरस',
        'Tomato Yellow Leaf Curl Virus': 'टोमॅटोचा पिवळा पान वक्र व्हायरस',
        'healthy': 'निरोगी',
        'Diseased': 'रोगी',
        'No treatment required': 'कोणताही उपचार आवश्यक नाही',
        'Maintain regular watering': 'नियमित पाणी देणे राखून ठेवा',
        'Disease detected': 'रोग आढळून आला',
        'Solution': 'समाधान',
        'Prevention': 'प्रतिबंध',
        'Symptoms': 'लक्षणे',
        'Recommendation': 'शिफारस',
        'Treatment': 'उपचार'
    },
    'Tamil': {
        'Apple scab': 'ஆப்பிள் தோல் நோய்',
        'Black rot': 'கருப்பு அழுகல்',
        'Cedar apple rust': 'சீடர் ஆப்பிள் பூஞ்சை',
        'Powdery mildew': 'பொடி பூஞ்சை',
        'Cercospora leaf spot': 'இலை பятி',
        'Common rust': 'சாதாரண பூஞ்சை',
        'Northern Leaf Blight': 'வடக்கு இலை சாவு',
        'Esca Black Measles': 'கருப்பு தட்டம்',
        'Bacterial spot': 'பாக்டீரியா புள்ளி',
        'Early blight': 'ஆரம்ப சாவு',
        'Late blight': 'தாமதமான சாவு',
        'Leaf scorch': 'இலை சுட்டுதல்',
        'Leaf Mold': 'இலை பூஞ்சை',
        'Septoria leaf spot': 'செப்டோரியா இலை புள்ளி',
        'Spider mites': 'சிலந்திப் பூச்சி',
        'Target Spot': 'இலக்குப் புள்ளி',
        'Tomato mosaic virus': 'தக்காளி மொசைக் வைரஸ்',
        'Tomato Yellow Leaf Curl Virus': 'தக்காளி மஞ்சள் இலை சுருட்ட வைரஸ்',
        'healthy': 'ஆரோக்கியமான',
        'Diseased': 'நோய்வாய்ப்பட்ட',
        'No treatment required': 'சிகிச்சை தேவையில்லை',
        'Maintain regular watering': 'வழக்கமான நீர்ப்பாசனத்தை பராமரிக்கவும்',
        'Disease detected': 'நோய் கண்டறியப்பட்டது',
        'Solution': 'தீர்வு',
        'Prevention': 'தடுப்பு',
        'Symptoms': 'அறிகுறிகள்',
        'Recommendation': 'பரிந்துரை',
        'Treatment': 'சிகிச்சை'
    },
    'Telugu': {
        'Apple scab': 'ఆపిల్ స్కాబ్',
        'Black rot': 'కాలుబద్దలు',
        'Cedar apple rust': 'సీడర్ ఆపిల్ తుప్పు',
        'Powdery mildew': 'పౌడర్ బొచ్చ',
        'Cercospora leaf spot': 'ఆకు నలుపు',
        'Common rust': 'సాధారణ తుప్పు',
        'Northern Leaf Blight': 'ఉత్తర ఆకు ఉండిపోవడం',
        'Esca Black Measles': 'నలుపు పశ్చిమం',
        'Bacterial spot': 'బాక్టీరియా నలుపు',
        'Early blight': 'ఆరంభ ఉండిపోవడం',
        'Late blight': 'చివరి ఉండిపోవడం',
        'Leaf scorch': 'ఆకు కాలుచేయుట',
        'Leaf Mold': 'ఆకు బొచ్చ',
        'Septoria leaf spot': 'సెప్టోరియా ఆకు నలుపు',
        'Spider mites': 'గిలక కీటకాలు',
        'Target Spot': 'లక్ష్య నలుపు',
        'Tomato mosaic virus': 'టమోటా మొజాయిక్ వైరస్',
        'Tomato Yellow Leaf Curl Virus': 'టమోటా పసుపు ఆకు కర్లింగ్ వైరస్',
        'healthy': 'ఆరోగ్యకరమైన',
        'Diseased': 'వ్యాధిగ్రస్తమైన',
        'No treatment required': 'ఎటువంటి చికిత్స అవసరం లేదు',
        'Maintain regular watering': 'సాధారణ నీటిపానను నిర్వహించండి',
        'Disease detected': 'వ్యాధి కనుగొనబడింది',
        'Solution': 'పరిష్కారం',
        'Prevention': 'నిరోధం',
        'Symptoms': 'లక్షణాలు',
        'Recommendation': 'సిఫారసు',
        'Treatment': 'చికిత్స'
    }
}

TREATMENT_TRANSLATIONS = {
    'Gujarati': {
        'Remove fallen leaves': 'પતિત પર્ણ દૂર કરો',
        'Apply fungicides': 'ફંગીસાઇડ લાગુ કરો',
        'Use crop rotation': 'પાક રોટેશન વાપરો',
        'Spray copper bactericide': 'તાંબાનું બેક્ટેરીસાઇડ સ્પ્રે કરો',
        'Consult local expert': 'સ્થાનિક વિશેષજ્ञને સલાહ કરો',
        'Destroy infected plants': 'સંક્રમિત છોડ નષ્ટ કરો',
        'Avoid overhead watering': 'ઓવરહેડ પાણી આપવાનો ટાળો',
        'Practice crop rotation': 'પાક રોટેશનનો અભ્યાસ કરો'
    },
    'Hindi': {
        'Remove fallen leaves': 'गिरी हुई पत्तियों को हटाएं',
        'Apply fungicides': 'कवकनाशी लागू करें',
        'Use crop rotation': 'फसल चक्र का उपयोग करें',
        'Spray copper bactericide': 'तांबा जीवाणुनाशक छिड़कें',
        'Consult local expert': 'स्थानीय विशेषज्ञ से परामर्श करें',
        'Destroy infected plants': 'संक्रमित पौधों को नष्ट करें',
        'Avoid overhead watering': 'ओवरहेड पानी देने से बचें',
        'Practice crop rotation': 'फसल चक्र का पालन करें'
    },
    'Marathi': {
        'Remove fallen leaves': 'पडलेली पाने काढून टाका',
        'Apply fungicides': 'बुरशांनाशक लागू करा',
        'Use crop rotation': 'पिकांचा आवर्तन वापरा',
        'Spray copper bactericide': 'तांबे जिवाणूनाशक फवारा करा',
        'Consult local expert': 'स्थानिक तज्ञांचा सल्ला घ्या',
        'Destroy infected plants': 'संक्रमित झाड नष्ट करा',
        'Avoid overhead watering': 'ओव्हरहेड पाणी देणे टाळा',
        'Practice crop rotation': 'पिकांचा आवर्तन करा'
    },
    'Tamil': {
        'Remove fallen leaves': 'விழுந்த இலைகளை நீக்கவும்',
        'Apply fungicides': 'பூஞ்சை நாசினி பயன்படுத்தவும்',
        'Use crop rotation': 'பயிர் சுழற்சியைப் பயன்படுத்தவும்',
        'Spray copper bactericide': 'செப்பு பாக்டீரियா நாசினி தெளிக்கவும்',
        'Consult local expert': 'உள்ளூர் நிபுணரை அறிந்து கொள்ளவும்',
        'Destroy infected plants': 'संक्रमित பயிர்களை அழிக்கவும்',
        'Avoid overhead watering': 'மேல் நின்று நீர்ப்பாசனத்தை தவிர்க்கவும்',
        'Practice crop rotation': 'பயிர் சுழற்சியை பயிற்சி செய்யவும்'
    },
    'Telugu': {
        'Remove fallen leaves': 'జారిపడిన ఆకులను తీసివేయండి',
        'Apply fungicides': 'శిలీంధ్రనాశకాలను వర్తించండి',
        'Use crop rotation': 'ఫసల్ చక్రాన్ని ఉపయోగించండి',
        'Spray copper bactericide': 'కాపర్ బాక్టీరియనాశకాన్ని చిమ్మండి',
        'Consult local expert': 'స్థానిక నిపుణుడిని సంప్రదించండి',
        'Destroy infected plants': 'సంక్రమిత మొక్కలను నాశనం చేయండి',
        'Avoid overhead watering': 'ఓవర్‌హెడ్ నీటిపానను నివారించండి',
        'Practice crop rotation': 'ఫసల్ చక్రాన్ని అభ్యసించండి'
    }
}


def translate_text(text: str, source_language: str = 'en', target_language: str = 'gu') -> Optional[str]:
    """
    Translate text to target language.
    Falls back to pretranslated terms if API translation not available.
    
    Args:
        text: Text to translate
        source_language: Source language code (default 'en')
        target_language: Target language code (e.g., 'gu', 'hi')
    
    Returns:
        Translated text or original if translation unavailable
    """
    try:
        # Try using Google Translate via requests
        import requests
        
        source_lang = source_language
        target_lang_code = target_language
        
        if target_lang_code == 'en' or source_lang == target_lang_code:
            return text
        
        # Free translation endpoint (using MyMemory)
        try:
            url = f"https://api.mymemory.translated.net/get?q={text}&langpair={source_lang}|{target_lang_code}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['responseStatus'] == 200:
                    return data['responseData']['translatedText']
        except Exception as e:
            print(f"MyMemory translation failed: {e}")
        
        # Fallback to predefined translations
        if target_language in DISEASE_TRANSLATIONS:
            return DISEASE_TRANSLATIONS[target_language].get(text, text)
        
        return text
        
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def translate_disease_result(result: Dict, source_language: str = 'en', target_language: str = 'gu') -> Dict:
    """
    Translate entire disease prediction result.
    
    Args:
        result: Disease prediction result dict
        source_language: Source language code (default 'en')
        target_language: Target language code
    
    Returns:
        Result dict with translated fields
    """
    translated = result.copy()
    
    try:
        # Translate main fields
        if target_language != 'en':
            translated['disease'] = translate_text(result.get('disease', ''), source_language, target_language)
            translated['status'] = translate_text(result.get('status', ''), source_language, target_language)
            translated['description'] = translate_text(result.get('description', ''), source_language, target_language)
            translated['treatment'] = translate_text(result.get('treatment', ''), source_language, target_language)
    
    except Exception as e:
        print(f"Error translating disease result: {e}")
    
    translated['target_language'] = target_language
    return translated


def get_supported_languages() -> Dict[str, str]:
    """Get list of supported languages."""
    return {
        'en': 'English',
        'gu': 'Gujarati',
        'hi': 'Hindi',
        'mr': 'Marathi',
        'ta': 'Tamil',
        'te': 'Telugu'
    }
