import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
DATASET_DIR = "dataset/plantvillage dataset/color"
MODEL_SAVE_PATH = "model/trained_model.h5"

def evaluate():
    try:
        print("Loading model...")
        model = load_model(MODEL_SAVE_PATH)
        
        print("Setting up validation generator...")
        val_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
        validation_generator = val_datagen.flow_from_directory(
            DATASET_DIR,
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='validation'
        )
        
        print("Evaluating model...")
        loss, accuracy = model.evaluate(validation_generator)
        print(f"\\n--- RESULTS ---")
        print(f"Validation Accuracy: {accuracy * 100:.2f}%")
        print(f"Validation Loss: {loss:.4f}")
    except Exception as e:
        print(f"Error during evaluation: {e}")

if __name__ == "__main__":
    evaluate()
