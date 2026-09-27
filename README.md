# CropDiseaseVision - AI-Powered Crop Health Assistant

A machine learning application that identifies crop diseases from images and provides multilingual recommendations.

## Features

- **Disease Detection**: AI-powered crop disease identification from images
- **Multilingual Support**: Translations in 6 languages (English, Hindi, Gujarati, Marathi, Tamil, Telugu)
- **Voice Features**: Speech-to-text input and text-to-speech output
- **Confidence Scoring**: Prediction confidence levels
- **Analysis History**: Track recent predictions

## Supported Languages

- English
- Hindi (हिन्दी)
- Gujarati (ગુજરાતી)
- Marathi (मराठी)
- Tamil (தமிழ்)
- Telugu (తెలుగు)

## Project Structure

```
CropDiseaseVision/
├── frontend/                 # Web UI (HTML/CSS/JavaScript)
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── multilingual-style.css
├── backend/                  # Flask API
│   ├── app.py
│   ├── routes/
│   ├── services/
│   └── utils/
├── model/                    # ML model files
│   ├── trained_model.h5
│   └── labels.json
├── dataset/                  # Training data
├── saved_models/             # Backup models
├── tests/                    # Test files
├── utils/                    # Utility functions
└── notebooks/                # Jupyter notebooks
```

## Setup

### Prerequisites
- Python 3.8+
- Node.js (for frontend, optional)
- 4GB RAM minimum
- CUDA compatible GPU (optional, for faster inference)

### Installation

1. **Clone and setup**
   ```bash
   cd CropDiseaseVision
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   cd backend && pip install -r requirements.txt && cd ..
   ```

3. **Start the application**
   ```bash
   # Windows
   start_system.bat
   
   # Linux/Mac
   bash start.bat
   ```

4. **Access the application**
   - Open browser and navigate to `http://localhost:5000`

## Usage

### Web Interface
1. Select language from dropdown (top-right)
2. Upload crop disease image
3. Click "Predict" or use voice recording
4. View disease name, confidence, and recommendations in selected language
5. Click "Speak" to hear recommendations

### API Endpoints

**Predict Disease**
- URL: `POST /api/predict`
- Input: Image file
- Output: Disease name, confidence, recommendations

**Multilingual Translation**
- Automatic translation of results to selected language
- Translation powered by LibreTranslate API

## Configuration

### Language Mapping
Edit `frontend/script.js` to add/modify languages:

```javascript
const LANGUAGE_MAP = {
    'English': 'en',
    'Hindi': 'hi',
    'Gujarati': 'gu',
    'Marathi': 'mr',
    'Tamil': 'ta',
    'Telugu': 'te'
};
```

### Model Configuration
- Trained model: `model/trained_model.h5`
- Class labels: `model/labels.json`
- Update paths in `backend/app.py` if relocated

## Performance

- **Prediction Time**: ~200-500ms
- **Translation Time**: ~1-2s (cached)
- **Batch Processing**: Supported

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Change port in `backend/app.py` |
| Model not found | Verify `model/trained_model.h5` exists |
| Translation not working | Check internet connection, LibreTranslate API accessible |
| Speech not working | Allow microphone permissions, use Chrome/Edge |

## API Documentation

### Health Check
```
GET /api/health
Response: {"status": "ok"}
```

### Predict
```
POST /api/predict
Content-Type: multipart/form-data

Body: image file
Response: {
    "disease": "Tomato___Early_blight",
    "confidence": 0.95,
    "recommendations": ["...", "...", "..."]
}
```

## Technology Stack

**Frontend**
- HTML5, CSS3, JavaScript
- Font Awesome icons
- Responsive design

**Backend**
- Flask (Python)
- TensorFlow/Keras (ML)
- LibreTranslate (Translations)

**ML Model**
- CNN-based architecture
- Trained on PlantVillage dataset
- 38 crop-disease classes

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## License

This project is provided as-is for educational and research purposes.

## Support

For issues or questions:
1. Check troubleshooting section
2. Review browser console (F12) for errors
3. Ensure all dependencies installed

---

**Version**: 2.0  
**Last Updated**: May 2026

======================================================================
TRAINING SUMMARY
======================================================================

Epoch    Train Acc      Val Acc        Train Loss     Val Loss
----------------------------------------------------------------------
1        0.7234         0.6891         0.8234         0.9123
2        0.8123         0.7654         0.5234         0.6234
...
10       0.9234         0.8876         0.2134         0.3456

----------------------------------------------------------------------
✓ Final Training Accuracy:   0.9234 (92.34%)
✓ Final Validation Accuracy: 0.8876 (88.76%)
✓ Final Training Loss:       0.2134
✓ Final Validation Loss:     0.3456

✓ Best Validation Accuracy:  0.8876 (88.76%) at Epoch 8
======================================================================