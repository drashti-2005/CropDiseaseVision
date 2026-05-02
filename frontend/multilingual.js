/**
 * CropDiseaseVision v2.0 - Multilingual Support Module
 * Handles language selection, translation, and multilingual speech
 * Languages: English, Hindi, Gujarati, Marathi, Tamil, Telugu
 */

// Language Configuration
const LANGUAGES = {
    'English': {
        code: 'en',
        voice_code: 'en-US',
        speech_recognition: 'en-US'
    },
    'Hindi': {
        code: 'hi',
        voice_code: 'hi-IN',
        speech_recognition: 'hi-IN'
    },
    'Gujarati': {
        code: 'gu',
        voice_code: 'gu-IN',
        speech_recognition: 'gu-IN'
    },
    'Marathi': {
        code: 'mr',
        voice_code: 'mr-IN',
        speech_recognition: 'mr-IN'
    },
    'Tamil': {
        code: 'ta',
        voice_code: 'ta-IN',
        speech_recognition: 'ta-IN'
    },
    'Telugu': {
        code: 'te',
        voice_code: 'te-IN',
        speech_recognition: 'te-IN'
    }
};

let currentLanguage = 'English'; // Default language
let translatedResults = {}; // Cache for translated results

/**
 * Initialize multilingual support
 * - Set up language selector
 * - Update speech recognition language
 * - Load saved language preference
 */
function initializeMultilingual() {
    const languageSelector = document.getElementById('languageSelector');
    
    if (!languageSelector) {
        console.error('Language selector not found');
        return;
    }
    
    // Load saved language preference
    const savedLanguage = localStorage.getItem('selectedLanguage');
    if (savedLanguage && LANGUAGES[savedLanguage]) {
        currentLanguage = savedLanguage;
        languageSelector.value = currentLanguage;
    }
    
    // Update speech recognition language
    updateSpeechRecognitionLanguage(currentLanguage);
    
    // Listen for language changes
    languageSelector.addEventListener('change', (e) => {
        changeLanguage(e.target.value);
    });
    
    console.log(`Multilingual support initialized. Current language: ${currentLanguage}`);
}

/**
 * Change the application language
 */
function changeLanguage(languageName) {
    if (!LANGUAGES[languageName]) {
        console.error(`Language ${languageName} not supported`);
        return;
    }
    
    currentLanguage = languageName;
    localStorage.setItem('selectedLanguage', currentLanguage);
    
    // Update speech recognition language
    updateSpeechRecognitionLanguage(currentLanguage);
    
    console.log(`Language changed to: ${currentLanguage}`);
    
    // If there are current results, retranslate them
    if (!document.getElementById('result').classList.contains('hidden')) {
        retranslateCurrentResults();
    }
}

/**
 * Update speech recognition language dynamically
 */
function updateSpeechRecognitionLanguage(languageName) {
    if (!recognition) return;
    
    const langConfig = LANGUAGES[languageName];
    if (!langConfig) return;
    
    recognition.lang = langConfig.speech_recognition;
    console.log(`Speech recognition language set to: ${langConfig.speech_recognition}`);
}

/**
 * Translate text using backend translation endpoint
 */
async function translateText(text, targetLanguage = currentLanguage) {
    // If English, no translation needed
    if (targetLanguage === 'English') {
        return text;
    }
    
    // Check cache first
    const cacheKey = `${text}_${targetLanguage}`;
    if (translatedResults[cacheKey]) {
        return translatedResults[cacheKey];
    }
    
    try {
        const langCode = LANGUAGES[targetLanguage].code;
        
        const response = await fetch('http://127.0.0.1:5000/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                target_language: langCode
            })
        });
        
        if (!response.ok) {
            console.error(`Translation error: ${response.status}`);
            return text; // Fallback to original text
        }
        
        const data = await response.json();
        const translatedText = data.translated_text || text;
        
        // Cache the translation
        translatedResults[cacheKey] = translatedText;
        
        return translatedText;
        
    } catch (error) {
        console.error('Translation API error:', error);
        return text; // Fallback to original text
    }
}

/**
 * Translate the disease name with special formatting
 */
async function translateDiseaseName(diseaseName) {
    // Clean the disease name for display and translation
    const cleanName = diseaseName.replace(/___/g, ' ').replace(/_/g, ' ');
    
    if (currentLanguage === 'English') {
        return cleanName;
    }
    
    const translated = await translateText(cleanName, currentLanguage);
    return translated;
}

/**
 * Generate multilingual recommendations
 */
async function generateMultilingualRecommendations(disease) {
    const recommendations = {
        'Apple___Apple_scab': [
            'Apply fungicides containing captan or sulfur',
            'Remove infected leaves and dropped fruit',
            'Improve air circulation through pruning',
            'Water at the base to keep foliage dry'
        ],
        'Apple___healthy': [
            'Maintain current watering schedule',
            'Regularly prune for good air flow',
            'Apply preventive dormant oil in late winter'
        ],
        'Corn_(maize)___Common_rust_': [
            'Apply fungicides early when pustules first appear',
            'Plant rust-resistant corn varieties next season',
            'Ensure proper spacing for air circulation'
        ],
        'Corn_(maize)___healthy': [
            'Continue proper fertilization',
            'Maintain consistent watering',
            'Scout regularly for pests'
        ],
        'Potato___Early_blight': [
            'Remove infected leaves immediately',
            'Apply chlorothalonil or copper-based fungicide',
            'Practice crop rotation (avoid planting potatoes in the same spot)'
        ],
        'Potato___Late_blight': [
            'Apply metalaxyl or mancozeb fungicides',
            'Improve air circulation by proper spacing',
            'Remove and destroy infected plants immediately'
        ],
        'Potato___healthy': [
            'Maintain consistent soil moisture',
            'Hill potatoes properly',
            'Monitor for Colorado potato beetles'
        ],
        'Tomato___Bacterial_spot': [
            'Apply copper-based bactericides',
            'Avoid overhead watering (use drip irrigation)',
            'Remove and destroy heavily infected plants',
            "Rotate crops (don't plant tomatoes or peppers in the same spot for 2-3 years)"
        ],
        'Tomato___Early_blight': [
            'Remove infected leaves (especially lower ones touching the soil)',
            'Apply mancozeb or copper fungicide',
            'Water at soil level only to prevent splashing'
        ],
        'Tomato___healthy': [
            'Continue regular watering at the base',
            'Provide adequate support/staking',
            'Apply balanced fertilizer as needed'
        ],
        'default': [
            'Consult with local agricultural extension',
            'Monitor plant regularly for any changes',
            'Ensure proper irrigation and drainage',
            'Maintain field hygiene and remove weeds'
        ]
    };
    
    const actions = recommendations[disease] || recommendations['default'];
    
    // Translate each recommendation
    const translatedActions = await Promise.all(
        actions.map(action => translateText(action, currentLanguage))
    );
    
    return translatedActions;
}

/**
 * Retranslate current results to new language
 */
async function retranslateCurrentResults() {
    const diseaseName = document.getElementById('diseaseName').textContent;
    
    // Extract disease name (remove formatting)
    const cleanDisease = diseaseName.replace(/\s-\s/g, '___').replace(/\s/g, '_');
    
    // Translate disease name
    const translatedDisease = await translateDiseaseName(cleanDisease);
    document.getElementById('diseaseName').textContent = translatedDisease;
    
    // Translate recommendations
    const translatedRecommendations = await generateMultilingualRecommendations(cleanDisease);
    const actionsList = document.getElementById('actionsList');
    actionsList.innerHTML = translatedRecommendations.map(action => `<li>${action}</li>`).join('');
}

/**
 * Speak translated result using Web Speech API (Text-to-Speech)
 */
async function speakTranslatedResult() {
    const diseaseName = document.getElementById('diseaseName').textContent;
    const confidence = document.getElementById('confidenceLevel').textContent;
    
    if (!diseaseName) {
        console.error('No results to speak');
        return;
    }
    
    // Create speech text
    let speechText = `Disease detected: ${diseaseName}. Confidence: ${confidence}`;
    
    // Translate the speech text if not English
    if (currentLanguage !== 'English') {
        speechText = await translateText(speechText, currentLanguage);
    }
    
    // Get voice code for the language
    const voiceCode = LANGUAGES[currentLanguage].voice_code;
    
    // Create utterance
    const utterance = new SpeechSynthesisUtterance(speechText);
    utterance.lang = voiceCode;
    utterance.rate = 0.9; // Slightly slower for farmers to understand
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    
    // Speak
    try {
        window.speechSynthesis.cancel(); // Cancel any ongoing speech
        window.speechSynthesis.speak(utterance);
        console.log(`Speaking in ${currentLanguage}: ${speechText}`);
    } catch (error) {
        console.error('Text-to-speech error:', error);
        alert('Audio output not available in this browser');
    }
}

/**
 * Stop ongoing speech
 */
function stopSpeech() {
    if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
        console.log('Speech stopped');
    }
}

/**
 * Initialize play result button and attach multilingual speech
 */
function setupPlayResultButton() {
    const playResultBtn = document.getElementById('playResultBtn');
    
    if (!playResultBtn) {
        console.warn('Play result button not found');
        return;
    }
    
    playResultBtn.addEventListener('click', () => {
        speakTranslatedResult();
    });
    
    // Also show current language in button
    playResultBtn.addEventListener('mouseover', () => {
        playResultBtn.title = `Listen in ${currentLanguage}`;
    });
}

/**
 * Export translation functions for use in other modules
 */
window.multilingual = {
    initializeMultilingual,
    changeLanguage,
    getCurrentLanguage: () => currentLanguage,
    translateText,
    translateDiseaseName,
    generateMultilingualRecommendations,
    speakTranslatedResult,
    stopSpeech,
    updateSpeechRecognitionLanguage
};

// Initialize multilingual support when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initializeMultilingual();
    setupPlayResultButton();
    console.log('Multilingual module initialized');
});
