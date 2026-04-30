import os
import io
import json
from PIL import Image
import sys

# Setup paths
base_dir = r"D:\practical\AI\AI project\CropDiseaseVision"
model_path = os.path.join(base_dir, "model", "trained_model.h5")
class_indices_path = os.path.join(base_dir, "model", "labels.json")

sys.path.append(base_dir)
from backend.services.inference import run_inference, load_model, get_model_status

def test_inference():
    print("Loading model via service...")
    load_model()
    
    if not get_model_status():
        print("Model failed to load.")
        return

    print("Creating fake image...")
    # Create a blank 224x224 RGB image
    img = Image.new('RGB', (224, 224), color = 'red')

    print("Predicting...")
    result = run_inference(img)
    print(f"Prediction: {result['disease']} at {result['confidence']}")

if __name__ == "__main__":
    test_inference()
