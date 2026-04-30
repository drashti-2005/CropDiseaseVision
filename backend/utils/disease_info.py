# Disease info and treatments mapping
# This acts as a simple rule-based knowledge base

DISEASE_KNOWLEDGE = {
    "Apple___Apple_scab": {
        "status": "Diseased",
        "description": "Fungal disease causing dark, scabby lesions on leaves and fruit.",
        "treatment": "Remove fallen leaves. Apply fungicides like Captan or Mancozeb early in the season."
    },
    "Apple___healthy": {
        "status": "Healthy",
        "description": "The apple leaf is healthy.",
        "treatment": "No treatment required. Maintain regular watering and fertilization."
    },
    "Corn_(maize)___Common_rust_": {
        "status": "Diseased",
        "description": "Fungal infection creating reddish-brown pustules on both leaf surfaces.",
        "treatment": "Use rust-resistant varieties. Apply foliar fungicides if infection is severe early."
    },
    "Corn_(maize)___healthy": {
        "status": "Healthy",
        "description": "The corn leaf is healthy.",
        "treatment": "No treatment required. Ensure adequate nitrogen and water."
    },
    "Potato___Early_blight": {
        "status": "Diseased",
        "description": "Fungal disease causing target-like concentric rings on older leaves.",
        "treatment": "Use crop rotation. Apply copper-based fungicides or Chlorothalonil."
    },
    "Potato___Late_blight": {
        "status": "Diseased",
        "description": "Oomycete pathogen causing rapid decay, water-soaked spots, and white fuzz.",
        "treatment": "Destroy infected plants. Apply specialized fungicides like Metalaxyl immediately."
    },
    "Potato___healthy": {
        "status": "Healthy",
        "description": "The potato leaf is healthy.",
        "treatment": "No treatment required. Practice standard crop rotation."
    },
    "Tomato___Bacterial_spot": {
        "status": "Diseased",
        "description": "Bacterial disease causing small, water-soaked spots on leaves and fruit.",
        "treatment": "Spray copper bactericide. Avoid overhead watering to reduce spread."
    },
    "Tomato___Early_blight": {
        "status": "Diseased",
        "description": "Fungal infection with target-like spots starting from the bottom leaves.",
        "treatment": "Mulch the base of the plant. Apply preventative fungal sprays."
    },
    "Tomato___healthy": {
        "status": "Healthy",
        "description": "The tomato leaf is healthy.",
        "treatment": "No treatment required. Keep leaves dry by watering at the base."
    }
}

def get_disease_info(predicted_class_name):
    """
    Returns the status, description, and treatment for a given class name.
    If the class is not exactly found, attempts to provide a default.
    """
    if predicted_class_name in DISEASE_KNOWLEDGE:
        return DISEASE_KNOWLEDGE[predicted_class_name]
    
    # Fallback if the dataset had different class names
    status = "Healthy" if "healthy" in predicted_class_name.lower() else "Diseased"
    disease_friendly_name = predicted_class_name.replace("___", " - ").replace("_", " ")

    return {
        "status": status,
        "description": f"Detected {disease_friendly_name}.",
        "treatment": "Consult a local agricultural expert for customized treatment."
    }
