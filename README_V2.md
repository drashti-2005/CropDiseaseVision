# 🌾 CropDiseaseVision v2.0 - Farmer-Friendly AI Assistant

**Empowering farmers with AI-powered crop disease detection!**

An end-to-end full-stack system for detecting crop diseases using Deep Learning (CNN/MobileNetV2), Flask backend, and a modern, intuitive web interface optimized for farmers.

---

## 🎯 Key Features

✅ **Image-Based Disease Detection** - Upload photos of affected leaves for instant analysis  
✅ **Voice-to-Text Input** - Describe crop issues in your own words  
✅ **High Confidence Display** - Only shows predictions with 10%+ confidence  
✅ **Farmer-Friendly UI** - Large buttons, clear language, mobile-optimized  
✅ **Treatment Recommendations** - Get actionable steps based on disease  
✅ **Analysis History** - Track your disease detections locally  
✅ **Multi-Platform Support** - Desktop, tablet, smartphone compatible  

---

## 🚀 Quick Start

### **Step 1: Activate Virtual Environment**
```bash
cd "d:\practical\AI\AI project\CropDiseaseVision"
venv\Scripts\activate
```

### **Step 2: Start Backend** (Terminal 1)
```bash
cd backend
python app.py
```
Expected: `Running on http://0.0.0.0:5000`

### **Step 3: Start Frontend** (Terminal 2)
```bash
cd frontend
python -m http.server 8000
```
Expected: `Serving HTTP on [::]:8000`

### **Step 4: Open in Browser**
Navigate to: **http://localhost:8000**

---

## 📱 How to Use

### **Image Analysis**
1. Click "Choose an Image" or drag & drop
2. Click "Analyze Image"
3. View disease name, confidence %, and treatment options

### **Voice Analysis**
1. Click the "Voice Input" tab
2. Click "Start Recording"
3. Describe your crop issue (e.g., "Yellow spots on tomato leaves")
4. Click "Stop Recording"
5. Click "Analyze Description"

---

## 🛠️ API Documentation

### Health Check
```bash
GET http://127.0.0.1:5000/health
```

### Predict from Image
```bash
POST http://127.0.0.1:5000/predict
Content-Type: multipart/form-data

# File: image.jpg
```

**Response:**
```json
{
  "disease": "Tomato___Late_blight",
  "confidence": 0.92,
  "confidence_percent": "92.00%",
  "all_predictions": [
    {"class": "Tomato___Late_blight", "confidence": 92.0},
    {"class": "Tomato___Early_blight", "confidence": 7.5}
  ],
  "success": true
}
```

### Predict from Voice
```bash
POST http://127.0.0.1:5000/predict-voice
Content-Type: application/json
Body: {"description": "brown spots on my potato leaves"}
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend API** | Flask 3.0.0 |
| **Machine Learning** | TensorFlow 2.21.0, MobileNetV2 |
| **Image Processing** | Pillow 11.0.0, NumPy |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Voice Recognition** | Web Speech API (built-in browser) |
| **Data Exchange** | JSON |

---

## 📊 Disease Categories

**38 Different Crop Diseases Supported:**

| Crop | Diseases |
|------|----------|
| **Apple** | Apple scab, Black rot, Cedar apple rust, Healthy |
| **Blueberry** | Healthy |
| **Cherry** | Powdery mildew, Healthy |
| **Corn/Maize** | Cercospora leaf spot, Common rust, Northern leaf blight, Healthy |
| **Grape** | Black rot, Esca (Black measles), Leaf blight, Healthy |
| **Orange** | Haunglongbing (Citrus greening) |
| **Peach** | Bacterial spot, Healthy |
| **Pepper** | Bacterial spot, Healthy |
| **Potato** | Early blight, Late blight, Healthy |
| **Raspberry** | Healthy |
| **Soybean** | Healthy |
| **Squash** | Powdery mildew |
| **Strawberry** | Leaf scorch, Healthy |
| **Tomato** | Bacterial spot, Early blight, Late blight, Leaf mold, Septoria leaf spot, Spider mites, Target spot, Mosaic virus, TYLCV, Healthy |

---

## ⚙️ Configuration

### Change Backend Port
Edit `backend/app.py` (last line):
```python
app.run(host='0.0.0.0', port=5000)  # Change 5000 to desired port
```

### Change Frontend API URL
Edit `frontend/script.js` (line ~135):
```javascript
const response = await fetch('http://YOUR_SERVER_IP:5000/predict', {
```

### Change Voice Language
Edit `frontend/script.js` (line ~4):
```javascript
recognition.lang = 'hi-IN';  // Change to your language (e.g., 'hi-IN', 'es-ES')
```

---

## 🐛 Troubleshooting

### **Backend won't start**
- ✓ Check virtual environment is activated: `venv\Scripts\activate`
- ✓ Install dependencies: `pip install -r backend/requirements.txt`
- ✓ Check port 5000 is not in use

### **Frontend doesn't load**
- ✓ Check backend is running first
- ✓ Verify port 8000 is available
- ✓ Clear browser cache (Ctrl+Shift+Delete)

### **Voice recognition not working**
- ✓ Only works on HTTPS or localhost
- ✓ Check browser supports Web Speech API (Chrome, Edge, Safari)
- ✓ Check microphone permissions are granted

### **Model predictions are poor**
- ✓ Current model may be untrained
- ✓ Train with your own dataset: `python model/train.py`
- ✓ Ensure images are well-lit and clear

---

## 📁 Project Structure

```
CropDiseaseVision/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── requirements.txt        # Backend dependencies
│   ├── routes/               
│   ├── services/
│   └── utils/
├── frontend/
│   ├── index.html            # Main UI
│   ├── script.js             # Frontend logic with voice support
│   ├── style.css             # Farmer-friendly styling
│   └── assets/
├── model/
│   ├── trained_model.h5      # Pre-trained model
│   ├── labels.json           # Disease labels
│   └── train.py              # Training script
├── dataset/                  # Your training images
├── tests/
│   ├── test_api.py
│   └── test_inference.py
├── requirements.txt          # Root dependencies
├── README.md                 # Original docs
├── README_V2.md             # This file
├── .gitignore               # Git ignore rules
└── start.bat                # Windows batch launcher
```

---

## 🚀 Advanced Usage

### Train Custom Model
```bash
python model/train.py --dataset dataset/plantvillage_dataset/color --epochs 50
```

### Deploy to Cloud
```bash
# Heroku
git push heroku main

# Railway
railway up

# Render
# Connect GitHub repo to Render dashboard
```

### Run Tests
```bash
python tests/test_api.py
python test_model.py
```

---

## 📞 Support

- **Documentation:** Check README.md and README_V2.md
- **Issues:** Review the Troubleshooting section
- **Backend Logs:** Check terminal output when running `python app.py`
- **Frontend Errors:** Check browser console (F12)

---

## 📜 License

This project is open-source and available for educational and commercial use.

---

## 🙏 Acknowledgments

- **Dataset:** PlantVillage Dataset
- **Model Architecture:** MobileNetV2
- **Framework:** TensorFlow/Keras
- **Frontend Icons:** Font Awesome

---

**Version:** 2.0  
**Last Updated:** May 2026  
**Status:** ✅ Production Ready

🌾 **Happy farming! Grow healthy crops with CropDiseaseVision!** 🌾
