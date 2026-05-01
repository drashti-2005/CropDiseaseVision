import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import pandas as pd

# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5
MODEL_SAVE_PATH = "model/trained_model.h5"

# --- Dataset Configuration ---
# Choose between "csv" or "directory"
DATA_MODE = "directory"  

# 1. Directory Mode Settings (if DATA_MODE = "directory")
# Updated to point to your PlantVillage dataset folder
DATASET_DIR = "dataset/plantvillage dataset/color"

# 2. CSV Mode Settings (if DATA_MODE = "csv")
CSV_PATH = "../dataset/labels.csv"
CSV_IMAGES_DIR = "../dataset/images"
CSV_X_COL = "filename"      # The column containing image names
CSV_Y_COL = "label"         # The column containing disease labels

def build_model(num_classes):
    """
    Builds a Transfer Learning model using MobileNetV2 as the base.
    """
    # Load MobileNetV2 without the top classification layer
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=IMG_SIZE + (3,))
    
    # Freeze the base model
    base_model.trainable = False
    
    # Add custom head for our specific number of classes
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    model.compile(
        optimizer=Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def train_model():
    print("Loading data...")
    # Data Augmentation configuration
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        validation_split=0.2 # Use 20% for validation
    )
    val_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

    if DATA_MODE == "csv":
        if not os.path.exists(CSV_PATH):
            print(f"Error: CSV file '{CSV_PATH}' not found. Please verify your paths.")
            return
            
        print(f"Reading CSV dataset from {CSV_PATH}...")
        df = pd.read_csv(CSV_PATH)
        # Ensure filenames are treated as strings
        df[CSV_X_COL] = df[CSV_X_COL].astype(str)
        
        print("Setting up training generator from CSV...")
        train_generator = train_datagen.flow_from_dataframe(
            dataframe=df,
            directory=CSV_IMAGES_DIR,
            x_col=CSV_X_COL,
            y_col=CSV_Y_COL,
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='training'
        )
        
        print("Setting up validation generator from CSV...")
        validation_generator = val_datagen.flow_from_dataframe(
            dataframe=df,
            directory=CSV_IMAGES_DIR,
            x_col=CSV_X_COL,
            y_col=CSV_Y_COL,
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='validation'
        )
    else:
        # Directory mode
        if not os.path.exists(DATASET_DIR) or len(os.listdir(DATASET_DIR)) == 0:
            print(f"Error: Dataset directory '{DATASET_DIR}' not found or empty.")
            return

        print("Setting up training generator from directory...")
        train_generator = train_datagen.flow_from_directory(
            DATASET_DIR,
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='training'
        )

        print("Setting up validation generator from directory...")
        validation_generator = val_datagen.flow_from_directory(
            DATASET_DIR,
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='validation'
        )

    num_classes = len(train_generator.class_indices)
    print(f"Detected {num_classes} classes: {train_generator.class_indices}")

    # Save class indices to a file so inference knows the mapping
    import json
    with open('model/labels.json', 'w') as f:
        json.dump(train_generator.class_indices, f)

    print("Building model...")
    model = build_model(num_classes)
    
    print("Starting training loop...")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator
    )

    # Save the model
    model.save(MODEL_SAVE_PATH)
    print(f"Model saved to {MODEL_SAVE_PATH}")

    # Plot accuracy and loss
    plot_training(history)

def plot_training(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    
    epochs_range = range(len(acc))

    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.savefig('training_history.png')
    print("Saved training history plot to 'training_history.png'")

if __name__ == "__main__":
    train_model()
