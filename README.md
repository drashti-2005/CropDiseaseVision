# 🌾 Crop Disease Detection System using AI (Computer Vision)

An end-to-end full-stack AI system for detecting plant diseases using Deep Learning (CNN / MobileNetV2), a FastAPI backend, and a modern sleek Glassmorphism UI.


python -m http.server 3000
python -m uvicorn backend.app:app --reload
## 📁 Project Structure

```
CropDiseaseVision/
│
├── dataset/         # [Action Required] Place your custom image dataset here (e.g., PlantVillage).
│
├── model/           # ML Models and Training
│   ├── train.py     # Script to train MobileNetV2 on your dataset.
│   └── create_dummy_model.py # Script to create a dummy untrained model for UI testing.
│
├── backend/         # API Layer
│   └── main.py      # FastAPI application that runs the model prediction.
│
├── frontend/        # User Interface
│   ├── index.html   # Main web application.
│   ├── style.css    # Premium Glassmorphism aesthetic styles.
│   └── script.js    # Drag-and-drop & API communication logic.
│
├── utils/           # Helper Functions
│   ├── inference.py     # Preprocessing and prediction wrappers.
│   └── disease_info.py  # Rule-based treatments and disease data.
│
└── requirements.txt # Python dependencies.
```

---

## 🚀 Getting Started

Follow these steps to run the complete system locally.

### 1. Install Dependencies
Open a terminal in the `CropDiseaseVision` folder and install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Generate the Model

**Option A: Quick UI Testing (Dummy Model)**
If you just want to test the full-stack architecture without waiting to train a model:
```bash
python model/create_dummy_model.py
```
*(This generates `plant_disease_model.h5` and `class_indices.json` with random weights).*

**Option B: Train a Real Model**
1. Download a dataset like PlantVillage.
2. Structure it as `dataset/[Class Name]/image.jpg`.
3. Run the training script:
```bash
python model/train.py
```

### 3. Start the Backend Server (API)
Start the FastAPI server from the project root using `uvicorn`:
```bash
uvicorn backend.main:app --reload
```
The server will start at `http://127.0.0.1:8000`.
You can view the auto-generated API docs at `http://127.0.0.1:8000/docs`.

### 4. Open the Frontend UI
You don't need a frontend server! Simply open `frontend/index.html` in your web browser:
1. Double-click `frontend/index.html`
2. **OR** run a simple HTTP server (optional):
```bash
cd frontend
python -m http.server 3000
```
Then visit `http://localhost:3000`.

### 5. Detect Diseases!
- Drag and drop a leaf image into the UI upload zone.
- Click **Analyze Leaf**.
- View the prediction, confidence, health status, and AI-recommended treatments.

---

## 🌐 Deployment (Optional)

To push this live to the internet:

### **Backend (FastAPI)**
You can deploy your backend to platforms like **Render**, **Railway**, or **Heroku**:
1. Commit the code to GitHub.
2. Link the repository to Render/Railway.
3. Set the start command to: `gunicorn -k uvicorn.workers.UvicornWorker backend.main:app --bind 0.0.0.0:$PORT`
4. Make sure standard instance size has enough RAM for TensorFlow (usually > 1GB).

### **Frontend (HTML/JS)**
You can host your `frontend/` folder for free on static hosting sites:
- **Vercel**
- **Netlify**
- **GitHub Pages**
*(Remember to update the fetch URL in `script.js` to point to your live backend API URL instead of `http://127.0.0.1:8000`)*.
