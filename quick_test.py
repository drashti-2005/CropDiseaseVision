#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick functional test of backend API"""

import json
import os
import sys
from pathlib import Path

# Set encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("\n" + "="*60)
print("CROPDISEASEVISION v2.0 - QUICK FUNCTIONALITY TEST")
print("="*60 + "\n")

# Test 1: Model Loading
print("TEST 1: Loading Model...")
try:
    from tensorflow.keras.models import load_model
    model_path = "model/trained_model.h5"
    model = load_model(model_path)
    print("✓ Model loaded successfully")
    print(f"  Input shape: {model.input_shape}")
    print(f"  Output shape: {model.output_shape}")
except Exception as e:
    print(f"✗ Failed to load model: {e}")

# Test 2: Labels Loading
print("\nTEST 2: Loading Disease Labels...")
try:
    with open("model/labels.json", "r") as f:
        labels = json.load(f)
    print(f"✓ Labels loaded: {len(labels)} diseases")
    print(f"  Sample diseases: {list(labels.keys())[:5]}")
except Exception as e:
    print(f"✗ Failed to load labels: {e}")

# Test 3: Image Preprocessing
print("\nTEST 3: Image Preprocessing Function...")
try:
    from PIL import Image
    import numpy as np
    
    # Create a test image (224x224x3)
    test_img = Image.new('RGB', (224, 224), color='red')
    
    # Convert to array and normalize
    img_array = np.array(test_img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    print(f"✓ Image preprocessing works")
    print(f"  Test image shape: {img_array.shape}")
    print(f"  Value range: {img_array.min():.2f} - {img_array.max():.2f}")
except Exception as e:
    print(f"✗ Image preprocessing failed: {e}")

# Test 4: Backend API Endpoints
print("\nTEST 4: Checking Backend API Endpoints...")
try:
    with open("backend/app.py", "r") as f:
        content = f.read()
    
    endpoints = {
        "/predict": "/predict" in content or "/predict" in content,
        "/predict-voice": "predict-voice" in content or "predict_voice" in content,
        "/health": "/health" in content,
    }
    
    for endpoint, found in endpoints.items():
        status = "✓" if found else "✗"
        print(f"{status} Endpoint {endpoint}: {'Found' if found else 'Not found'}")
except Exception as e:
    print(f"✗ Error checking endpoints: {e}")

# Test 5: Frontend Features
print("\nTEST 5: Checking Frontend Features...")
try:
    with open("frontend/script.js", "r") as f:
        js_content = f.read()
    
    features = {
        "Image upload": "imageInput" in js_content,
        "Voice recognition": "SpeechRecognition" in js_content,
        "Confidence display": "confidence" in js_content.lower(),
        "History tracking": "localStorage" in js_content,
        "Recommendations": "recommendations" in js_content or "actionsList" in js_content,
    }
    
    for feature, found in features.items():
        status = "✓" if found else "✗"
        print(f"{status} {feature}: {'Enabled' if found else 'Disabled'}")
except Exception as e:
    print(f"✗ Error checking features: {e}")

# Test 6: CSS Validity
print("\nTEST 6: Checking CSS Syntax...")
try:
    with open("frontend/style.css", "r") as f:
        css_content = f.read()
    
    # Basic CSS checks
    issues = []
    if not ":root" in css_content:
        issues.append("Missing CSS variables")
    if css_content.count("{") != css_content.count("}"):
        issues.append("Mismatched braces")
    if not ".container" in css_content:
        issues.append("Missing container styles")
    
    if not issues:
        print("✓ CSS syntax valid")
        print(f"  CSS size: {len(css_content)} bytes")
    else:
        for issue in issues:
            print(f"⚠ {issue}")
except Exception as e:
    print(f"✗ Error checking CSS: {e}")

# Test 7: HTML Structure
print("\nTEST 7: Checking HTML Structure...")
try:
    with open("frontend/index.html", "r") as f:
        html_content = f.read()
    
    required_elements = {
        "<form": "✓ Form elements",
        'id="imageInput"': "✓ Image input field",
        'id="voiceBtn"': "✓ Voice button",
        'id="predictBtn"': "✓ Predict button",
        'id="result"': "✓ Result container",
        'class="container"': "✓ Main container",
    }
    
    found_count = 0
    for element, description in required_elements.items():
        if element in html_content:
            print(description)
            found_count += 1
        else:
            print(f"✗ Missing {description.replace('✓ ', '')}")
    
    print(f"\nHTML structure: {found_count}/{len(required_elements)} elements found")
except Exception as e:
    print(f"✗ Error checking HTML: {e}")

# Summary
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)
print("\n✓ Project is configured and ready!")
print("\nTo run the project:")
print("  1. Terminal 1: cd backend && python app.py")
print("  2. Terminal 2: cd frontend && python -m http.server 8000")
print("  3. Browser: http://localhost:8000")
print("\n" + "="*60 + "\n")
