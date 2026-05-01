// Initialize Speech Recognition
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;

if (SpeechRecognition) {
    try {
        recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;
    } catch (e) {
        console.error("SpeechRecognition initialization failed:", e);
    }
}

// DOM Elements
const imageInput = document.getElementById('imageInput');
const imagePreview = document.getElementById('imagePreview');
const predictBtn = document.getElementById('predictBtn');
const voiceBtn = document.getElementById('voiceBtn');
const voicePredictBtn = document.getElementById('voicePredictBtn');
const loading = document.getElementById('loading');
const result = document.getElementById('result');
const diseaseNameSpan = document.getElementById('diseaseName');
const confidenceLevelSpan = document.getElementById('confidenceLevel');
const confidenceBar = document.getElementById('confidenceBar');
const errorDiv = document.getElementById('error');
const errorMessage = document.getElementById('errorMessage');
const resetBtn = document.getElementById('resetBtn');
const voiceStatus = document.getElementById('voiceStatus');
const voiceTranscript = document.getElementById('voiceTranscript');
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const actionsList = document.getElementById('actionsList');
const historyList = document.getElementById('historyList');

let voiceTranscriptText = '';
let analysisHistory = [];

// Tab Switching
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');
        
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        
        btn.classList.add('active');
        document.getElementById(`${tabName}-tab`).classList.add('active');
    });
});

// Image Upload with Drag & Drop
imageInput.addEventListener('change', handleImageUpload);

document.querySelector('.upload-section').addEventListener('dragover', (e) => {
    e.preventDefault();
    document.querySelector('.upload-section').style.borderColor = '#f39c12';
});

document.querySelector('.upload-section').addEventListener('dragleave', (e) => {
    document.querySelector('.upload-section').style.borderColor = '#27ae60';
});

document.querySelector('.upload-section').addEventListener('drop', (e) => {
    e.preventDefault();
    imageInput.files = e.dataTransfer.files;
    handleImageUpload();
});

function handleImageUpload() {
    const file = imageInput.files[0];
    
    clearResults();
    
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
            predictBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    } else {
        showError('Please select a valid image file (JPG, PNG, etc.)');
        imagePreview.style.display = 'none';
        predictBtn.disabled = true;
    }
}

// Voice Recognition
voiceBtn.addEventListener('click', () => {
    if (!recognition) {
        showError('Voice recognition is not supported in this browser. Please use Chrome or Edge.');
        return;
    }
    
    if (voiceBtn.classList.contains('recording')) {
        recognition.abort();
        voiceBtn.classList.remove('recording');
        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i> Start Recording';
        voiceStatus.textContent = 'Recording stopped';
    } else {
        voiceStatus.textContent = 'Listening...';
        voiceTranscript.style.display = 'none';
        voiceBtn.classList.add('recording');
        voiceBtn.innerHTML = '<i class="fas fa-stop-circle"></i> Stop Recording';
        recognition.start();
    }
});

if (recognition) {
    recognition.onresult = (event) => {
        voiceTranscriptText = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            voiceTranscriptText += event.results[i][0].transcript;
        }
        voiceTranscript.textContent = voiceTranscriptText;
        voiceTranscript.style.display = 'block';
        voiceStatus.textContent = 'Processing...';
    };

    recognition.onend = () => {
        voiceBtn.classList.remove('recording');
        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i> Start Recording';
        voiceStatus.textContent = 'Ready to analyze';
        voicePredictBtn.disabled = !voiceTranscriptText;
    };

    recognition.onerror = (event) => {
        showError(`Voice recognition error: ${event.error}`);
        voiceBtn.classList.remove('recording');
        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i> Start Recording';
    };
}

// Image Prediction
predictBtn.addEventListener('click', predictFromImage);

// Voice Prediction
voicePredictBtn.addEventListener('click', predictFromVoice);

async function predictFromImage() {
    const file = imageInput.files[0];
    
    if (!file) {
        showError('Please select an image first');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    showLoading(true);
    
    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError(`Failed to connect to backend. Make sure the server is running on http://127.0.0.1:5000`);
    } finally {
        showLoading(false);
    }
}

async function predictFromVoice() {
    if (!voiceTranscriptText) {
        showError('Please record a voice description first');
        return;
    }
    
    showLoading(true);
    
    try {
        // Send voice description to backend
        const response = await fetch('http://127.0.0.1:5000/predict-voice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ description: voiceTranscriptText })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        displayResults(data, 'voice');
        
    } catch (error) {
        console.error('Error:', error);
        showError('Voice-based detection not yet available or backend error');
    } finally {
        showLoading(false);
    }
}

function displayResults(data, source = 'image') {
    clearResults();
    
    // Extract disease name and confidence
    const diseaseName = data.disease || 'Unknown';
    const confidence = (data.confidence * 100).toFixed(2);
    
    // Format display name
    const formattedName = diseaseName.replace(/___/g, ' - ').replace(/_/g, ' ');
    
    // Show results
    diseaseNameSpan.textContent = formattedName;
    confidenceLevelSpan.textContent = `${confidence}%`;
    confidenceBar.style.width = `${confidence}%`;
    
    // Generate recommendations based on disease
    generateRecommendations(diseaseName);
    
    // Add to history
    addToHistory(diseaseName, confidence, source);
    
    result.classList.remove('hidden');
}

function generateRecommendations(disease) {
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
    
    actionsList.innerHTML = actions.map(action => `<li>${action}</li>`).join('');
}

function addToHistory(disease, confidence, source) {
    const timestamp = new Date().toLocaleTimeString();
    const historyItem = {
        disease,
        confidence,
        source,
        timestamp
    };
    
    analysisHistory.unshift(historyItem);
    if (analysisHistory.length > 10) analysisHistory.pop();
    
    updateHistoryUI();
    saveToLocalStorage();
}

function updateHistoryUI() {
    historyList.innerHTML = analysisHistory.map((item, index) => `
        <div class="history-item" onclick="replayAnalysis(${index})">
            <div class="disease">${item.disease.replace(/___/g, ' - ').replace(/_/g, ' ')}</div>
            <div class="confidence">${item.confidence}% | ${item.source}</div>
            <div class="time" style="font-size: 0.8rem; color: #95a5a6; margin-top: 5px;">${item.timestamp}</div>
        </div>
    `).join('');
}

function saveToLocalStorage() {
    localStorage.setItem('analysisHistory', JSON.stringify(analysisHistory));
}

function loadFromLocalStorage() {
    const saved = localStorage.getItem('analysisHistory');
    if (saved) {
        analysisHistory = JSON.parse(saved);
        updateHistoryUI();
    }
}

function replayAnalysis(index) {
    const item = analysisHistory[index];
    const formattedName = item.disease.replace(/___/g, ' - ').replace(/_/g, ' ');
    diseaseNameSpan.textContent = formattedName;
    confidenceLevelSpan.textContent = `${item.confidence}%`;
    confidenceBar.style.width = `${item.confidence}%`;
    generateRecommendations(item.disease);
    result.classList.remove('hidden');
    window.scrollTo({ top: result.offsetTop, behavior: 'smooth' });
}

// UI Helpers
function showLoading(show) {
    if (show) {
        loading.classList.remove('hidden');
        result.classList.add('hidden');
        errorDiv.classList.add('hidden');
    } else {
        loading.classList.add('hidden');
    }
}

function showError(message) {
    errorMessage.textContent = message;
    errorDiv.classList.remove('hidden');
    result.classList.add('hidden');
    loading.classList.add('hidden');
}

function clearResults() {
    result.classList.add('hidden');
    errorDiv.classList.add('hidden');
    loading.classList.add('hidden');
}

// Reset Button
resetBtn.addEventListener('click', () => {
    imageInput.value = '';
    imagePreview.style.display = 'none';
    predictBtn.disabled = true;
    voiceTranscriptText = '';
    voiceTranscript.style.display = 'none';
    voiceTranscript.textContent = '';
    voiceStatus.textContent = '';
    voicePredictBtn.disabled = true;
    clearResults();
    
    // Switch back to image tab
    tabBtns[0].click();
});

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    loadFromLocalStorage();
    console.log('CropDiseaseVision v2.0 Ready!');
});
