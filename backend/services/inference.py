import os
import json
import numpy as np
import tensorflow as tf
from backend.utils.image_preprocessing import preprocess_image
from backend.utils.disease_info import get_disease_info

# Model singleton
_model = None
_class_indices = None

def load_model():
    global _model, _class_indices
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    MODEL_PATH = os.path.join(base_dir, 'model', 'trained_model.h5')
    CLASS_INDICES_PATH = os.path.join(base_dir, 'model', 'labels.json')

    try:
        if os.path.exists(MODEL_PATH):
            _model = tf.keras.models.load_model(MODEL_PATH, compile=False)
            print("Model loaded successfully from:", MODEL_PATH)
        else:
            print("WARNING: Model file not found:", MODEL_PATH)

        if os.path.exists(CLASS_INDICES_PATH):
            with open(CLASS_INDICES_PATH, 'r') as f:
                _class_indices = json.load(f)
            print("Class indices loaded from:", CLASS_INDICES_PATH)
        else:
            print("WARNING: Class indices not found:", CLASS_INDICES_PATH)

    except Exception as e:
        print(f"Error loading model: {e}")

def get_model_status():
    return _model is not None and _class_indices is not None

def run_inference(image):
    if not get_model_status():
        raise Exception("Model is not loaded. Ensure trained_model.h5 and labels.json exist.")
        
    img_batch = preprocess_image(image)
    preds = _model.predict(img_batch)
    class_idx = np.argmax(preds[0])
    confidence = float(np.max(preds[0]))
    
    idx_to_class = {v: k for k, v in _class_indices.items()}
    class_name = idx_to_class.get(class_idx, "Unknown")
    
    knowledge = get_disease_info(class_name)
    
    return {
        "disease": class_name.replace("___", " - ").replace("_", " "),
        "confidence": f"{round(confidence * 100, 2)}%",
        "status": knowledge["status"],
        "description": knowledge["description"],
        "treatment": knowledge["treatment"],
        "raw_class": class_name
    }
