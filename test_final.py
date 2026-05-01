#!/usr/bin/env python3
"""Final project test - Simple ASCII version"""

import json
import os
from pathlib import Path

print("\n" + "="*60)
print("CROPDISEASEVISION v2.0 - FINAL PROJECT TEST")
print("="*60 + "\n")

results = {}

# TEST 1
print("TEST 1: Project Structure")
files_needed = [
    'backend/app.py', 'frontend/index.html', 'frontend/style.css',
    'frontend/script.js', 'model/trained_model.h5', 'model/labels.json'
]
test1_pass = all(Path(f).exists() for f in files_needed)
results['Structure'] = test1_pass
print(f"Result: {'PASS' if test1_pass else 'FAIL'}")

# TEST 2
print("\nTEST 2: Model Files")
try:
    with open('model/labels.json', 'r') as f:
        labels = json.load(f)
    model_size = Path('model/trained_model.h5').stat().st_size / (1024*1024)
    print(f"  - Model: {model_size:.1f} MB")
    print(f"  - Disease classes: {len(labels)}")
    results['Model'] = True
    print("Result: PASS")
except Exception as e:
    results['Model'] = False
    print(f"Result: FAIL - {e}")

# TEST 3
print("\nTEST 3: Backend API Endpoints")
try:
    with open('backend/app.py', 'r') as f:
        content = f.read()
    has_predict = '/predict' in content
    has_voice = 'predict' in content and 'voice' in content
    has_health = '/health' in content
    test3_pass = has_predict and has_voice and has_health
    results['Backend'] = test3_pass
    print(f"  - /predict: {'YES' if has_predict else 'NO'}")
    print(f"  - /predict-voice: {'YES' if has_voice else 'NO'}")
    print(f"  - /health: {'YES' if has_health else 'NO'}")
    print(f"Result: {'PASS' if test3_pass else 'FAIL'}")
except Exception as e:
    results['Backend'] = False
    print(f"Result: FAIL - {e}")

# TEST 4
print("\nTEST 4: Frontend Features")
try:
    with open('frontend/script.js', 'r') as f:
        js = f.read()
    with open('frontend/index.html', 'r') as f:
        html = f.read()
    
    features = {
        'Image Upload': 'imageInput' in html,
        'Voice Input': 'voiceBtn' in html,
        'Predictions': 'predictBtn' in html,
        'Results Display': 'result' in html,
        'History': 'history' in html or 'localStorage' in js,
    }
    
    for feat, present in features.items():
        print(f"  - {feat}: {'YES' if present else 'NO'}")
    
    results['Frontend'] = all(features.values())
    print(f"Result: {'PASS' if results['Frontend'] else 'FAIL'}")
except Exception as e:
    results['Frontend'] = False
    print(f"Result: FAIL - {e}")

# TEST 5
print("\nTEST 5: CSS Styling")
try:
    with open('frontend/style.css', 'r') as f:
        css = f.read()
    
    checks = {
        'Root variables': ':root' in css,
        'Container styles': '.container' in css,
        'Button styles': 'button' in css or '.btn' in css,
        'Responsive design': '@media' in css,
    }
    
    for check, passed in checks.items():
        print(f"  - {check}: {'YES' if passed else 'NO'}")
    
    results['CSS'] = all(checks.values())
    print(f"Result: {'PASS' if results['CSS'] else 'FAIL'}")
except Exception as e:
    results['CSS'] = False
    print(f"Result: FAIL - {e}")

# SUMMARY
print("\n" + "="*60)
print("FINAL SUMMARY")
print("="*60)

passed = sum(1 for v in results.values() if v)
total = len(results)

for test_name, passed_test in results.items():
    status = "PASS" if passed_test else "FAIL"
    print(f"{test_name:.<40} {status}")

print("\n" + "="*60)
print(f"OVERALL: {passed}/{total} Tests Passed")
print("="*60)

if passed == total:
    print("\n[SUCCESS] Project is READY TO RUN!\n")
    print("START THE PROJECT:")
    print("  Terminal 1: cd backend && python app.py")
    print("  Terminal 2: cd frontend && python -m http.server 8000")
    print("  Browser:   http://localhost:8000\n")
else:
    print(f"\n[WARNING] {total - passed} test(s) failed. Fix issues and retry.\n")

print("="*60 + "\n")
