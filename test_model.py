import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

# Import our custom modules
from utils.data_loader import get_50_random_images
from utils.preprocessing import preprocess_images

def train_test_split_custom(X, y, test_size=0.2):
    """ Custom train/test split to avoid needing scikit-learn dependency limit. """
    # Shuffle indices ensures a mix of classes
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    
    split_idx = int(len(X) * (1 - test_size))
    
    train_idx = indices[:split_idx]
    test_idx = indices[split_idx:]
    
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]

def build_model(num_classes):
    """ Builds a lightweight MobileNetV2 model """
    # Load MobileNetV2 without the top layer
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False  # Freeze base model for quick testing
    
    # Add custom classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',  # Target labels are integers not one-hot encoded
        metrics=['accuracy']
    )
    return model

def main():
    print("--- 🚀 Starting ML Pipeline Test ---")
    
    # ======== Step 1 & 2: Load Dataset and Select 50 Sample ========
    # Handles spaces in folder name correctly naturally.
    dataset_path = os.path.join("dataset", "plantvillage dataset", "color")
    
    # Check if path exists
    if not os.path.exists(dataset_path):
        print(f"❌ Error: Could not find dataset path at '{dataset_path}'")
        return
        
    print(f"1 & 2. Loading 50 random images from {dataset_path}...")
    image_paths, labels = get_50_random_images(dataset_path, num_images=50)
    
    if len(image_paths) == 0:
        print("❌ Error: No images found. Check your dataset path.")
        return
        
    print(f"   ✅ Successfully selected {len(image_paths)} images.")
    
    # ======== Step 3: Preprocessing ========
    print("3. Preprocessing images (Resize, Normalize, Convert to NumPy)...")
    X, y_encoded, class_mapping = preprocess_images(image_paths, labels)
    num_classes = len(class_mapping)
    print(f"   ✅ Processed data shape: {X.shape}. Found {num_classes} unique classes.")
    
    # ======== Step 4: Train/Test Split (80/20) ========
    print("4. Splitting data into 80% Train and 20% Test...")
    X_train, X_test, y_train, y_test = train_test_split_custom(X, y_encoded, test_size=0.2)
    print(f"   ✅ Train size: {len(X_train)}, Test size: {len(X_test)}")
    
    # ======== Step 5: Build Model ========
    print("5. Building lightweight MobileNetV2 model...")
    model = build_model(num_classes)
    print("   ✅ Model built successfully.")
    
    # ======== Step 6: Train (1-3 epochs) ========
    print("6. Training model for 3 epochs...")
    history = model.fit(
        X_train, y_train, 
        epochs=3, 
        validation_data=(X_test, y_test),
        batch_size=8,
        verbose=1 # Prints accuracy and loss
    )
    print("   ✅ Training completed!")
    print(f"   Final Train Accuracy: {history.history['accuracy'][-1]:.4f}")
    print(f"   Final Train Loss: {history.history['loss'][-1]:.4f}")
    print(f"   Final Val Accuracy: {history.history['val_accuracy'][-1]:.4f}")
    
    # ======== Step 7: Test with one sample ========
    print("\n7. Testing pipeline with one sample image...")
    # Take first image from test set, keep batch dimension
    sample_img = X_test[0:1] 
    actual_class_id = y_test[0]
    actual_class_name = class_mapping[actual_class_id]
    
    predictions = model.predict(sample_img)
    predicted_class_id = np.argmax(predictions[0])
    confidence = np.max(predictions[0]) * 100
    predicted_class_name = class_mapping[predicted_class_id]
    
    print("-" * 40)
    print("🧪 PREDICTION RESULTS:")
    print(f"   Actual Class   : {actual_class_name}")
    print(f"   Predicted Class: {predicted_class_name}")
    print(f"   Confidence %   : {confidence:.2f}%")
    print("-" * 40)
    
    print("\n🎉 ML PIPELINE TEST SUCCESSFUL! 🎉")

if __name__ == "__main__":
    main()
