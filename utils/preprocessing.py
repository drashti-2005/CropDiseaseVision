import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

def preprocess_images(image_paths, labels, target_size=(224, 224)):
    """
    Reads dataset paths, resizes them, normalizes to 0-1, and 
    encodes the string labels into categorical integers.
    """
    processed_images = []
    valid_labels = []
    
    for img_path, label in zip(image_paths, labels):
        try:
            # Read and resize image using Keras load_img
            img = load_img(img_path, target_size=target_size)
            
            # Convert to numpy array
            img_array = img_to_array(img)
            
            # Normalize pixel values (0-1)
            img_array = img_array / 255.0
            
            processed_images.append(img_array)
            valid_labels.append(label)
        except Exception as e:
            print(f"Error loading {img_path}: {e}")
            
    # Convert to NumPy array
    X = np.array(processed_images, dtype=np.float32)
    
    # Encode labels manually
    unique_classes = sorted(list(set(valid_labels)))
    class_indices = {class_name: idx for idx, class_name in enumerate(unique_classes)}
    
    y_encoded = np.array([class_indices[label] for label in valid_labels])
    
    # Reverse lookup to get class names during inference
    indices_class = {idx: class_name for class_name, idx in class_indices.items()}
    
    return X, y_encoded, indices_class
