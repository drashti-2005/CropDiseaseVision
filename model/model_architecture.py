import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model

# Run this script to generate a dummy model file and mock class indices, 
# so you can run the FastAPI backend immediately without needing to train first!

MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), "plant_disease_model.h5")
CLASS_INDICES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "class_indices.json")

# Sample classes based on PlantVillage dataset
DUMMY_CLASSES = {
    "Apple___Apple_scab": 0,
    "Apple___healthy": 1,
    "Corn_(maize)___Common_rust_": 2,
    "Corn_(maize)___healthy": 3,
    "Potato___Early_blight": 4,
    "Potato___Late_blight": 5,
    "Potato___healthy": 6,
    "Tomato___Bacterial_spot": 7,
    "Tomato___Early_blight": 8,
    "Tomato___healthy": 9
}

def create_dummy():
    print("Creating mock class indices...")
    with open(CLASS_INDICES_PATH, 'w') as f:
        json.dump(DUMMY_CLASSES, f)

    num_classes = len(DUMMY_CLASSES)
    
    print("Building untrained dummy model for demonstration...")
    # Just an untrained layout to satisfy loading in the backend
    base_model = MobileNetV2(weights=None, include_top=False, input_shape=(224, 224, 3))
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    
    model.save(MODEL_SAVE_PATH)
    print(f"Dummy model saved successfully to {MODEL_SAVE_PATH}!")
    print("\nYou can now start the FastAPI server to test the UI.")

if __name__ == "__main__":
    create_dummy()
