import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array

# MobileNetV2 requires (224, 224)
TARGET_SIZE = (224, 224)

def preprocess_image(image: Image.Image):
    """
    Resizes and normalizes the image for the model.
    """
    if image.mode != "RGB":
        image = image.convert("RGB")
        
    image = image.resize(TARGET_SIZE)
    img_array = img_to_array(image)
    
    # Scale pixels to [0, 1] as used in ImageDataGenerator during training
    img_array = img_array / 255.0
    
    # Add batch dimension: (1, 224, 224, 3)
    img_batch = np.expand_dims(img_array, axis=0)
    
    return img_batch
