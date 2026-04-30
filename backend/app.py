import os
import json
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image

app = Flask(__name__)
# Enable CORS so the frontend can make requests to this API structure
CORS(app)

# Define paths relative to the current file structure ensuring correct model and labels loading
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "trained_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "model", "labels.json")

# Load model and labels at startup (Global scope)
model = None
class_labels = {}

try:
    print(f"Loading model from {MODEL_PATH}...")
    # Requires an already trained tensorflow keras model structure
    model = load_model(MODEL_PATH)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

try:
    print(f"Loading labels from {LABELS_PATH}...")
    with open(LABELS_PATH, "r") as f:
        # labels.json format: {"Disease_Name": index, ...}
        # We need a mapping from index to "Disease Name"
        labels_dict = json.load(f)
        
        # Swapping key/value so index is the key
        # Removing underscores to format nicely e.g., 'Apple___Apple_scab' -> 'Apple - Apple scab'
        class_labels = {int(v): k.replace("___", " - ").replace("_", " ") for k, v in labels_dict.items()}
    print("Labels loaded successfully.")
except Exception as e:
    print(f"Error loading labels: {e}")

def preprocess_image(image, target_size=(224, 224)):
    """Preprocess the input image before feeding it to the model."""
    # Ensure image is in RGB format correctly 
    if image.mode != "RGB":
        image = image.convert("RGB")
        
    # Resize to the target size expected by the model (224x224)
    image = image.resize(target_size)
    
    # Convert image to numpy array
    image_array = img_to_array(image)
    
    # Normalize pixel values to [0, 1] as usually required by keras models
    image_array = image_array / 255.0
    
    # Expand dimensions to match model input shape (batch_size, height, width, channels)
    image_array = np.expand_dims(image_array, axis=0)
    
    return image_array

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint to predict crop disease from an image."""
    # Handle if model wasn't loaded
    if model is None:
        return jsonify({"error": "Model failed to load on the server. Please check the backend."}), 500

    # Validate that front-end included a 'file' in request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400
    
    file = request.files['file']
    
    # Check if a filename is valid and not empty
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400
        
    try:
        # Read the image file using PIL
        image = Image.open(file.stream)
        
        # Run preprocessing to make data model-compatible
        processed_image = preprocess_image(image)
        
        # Predict the class probabilities
        predictions = model.predict(processed_image)
        
        # Extract the index of the highest probability prediction
        predicted_class_index = int(np.argmax(predictions, axis=1)[0])
        
        # Calculate matching confidence percentage
        confidence = float(predictions[0][predicted_class_index]) * 100
        
        # Resolve the string label from index, fallback to Unknown otherwise
        disease_name = class_labels.get(predicted_class_index, "Unknown Disease")
        
        # Return cleanly formatted JSON back to the caller
        return jsonify({
            "disease": disease_name,
            "confidence": f"{confidence:.2f}%"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Easy verification endpoint to check the service works without file uploads
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({"message": "Crop Disease Detection API is running. Use POST /predict to test."})
        
    # Bound to all interfaces on port 5000 with Debug on for easy dev testing 
    app.run(host='0.0.0.0', port=5000, debug=True)
