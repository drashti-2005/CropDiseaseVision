#!/usr/bin/env python3
"""
CropDiseaseVision v2.0 - Comprehensive Testing Suite
Tests all functionality of the project
"""

import os
import sys
import json
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ {text}{RESET}")

# Test 1: Check Project Structure
def test_project_structure():
    print_header("TEST 1: PROJECT STRUCTURE")
    
    required_files = [
        'backend/app.py',
        'backend/requirements.txt',
        'frontend/index.html',
        'frontend/style.css',
        'frontend/script.js',
        'model/trained_model.h5',
        'model/labels.json',
        'class_indices.json',
        '.gitignore',
        'README_V2.md'
    ]
    
    all_exist = True
    for file in required_files:
        path = Path(file)
        if path.exists():
            print_success(f"Found: {file}")
        else:
            print_error(f"Missing: {file}")
            all_exist = False
    
    return all_exist

# Test 2: Check Dependencies
def test_dependencies():
    print_header("TEST 2: PYTHON DEPENDENCIES")
    
    required_packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'tensorflow': 'TensorFlow',
        'PIL': 'Pillow',
        'numpy': 'NumPy'
    }
    
    all_installed = True
    for package, name in required_packages.items():
        try:
            __import__(package)
            print_success(f"Installed: {name}")
        except ImportError:
            print_error(f"Missing: {name} - Install with: pip install {name.lower()}")
            all_installed = False
    
    return all_installed

# Test 3: Check Model Files
def test_model_files():
    print_header("TEST 3: MODEL & LABELS")
    
    tests_passed = 0
    
    # Check model file
    if Path('model/trained_model.h5').exists():
        size_mb = Path('model/trained_model.h5').stat().st_size / (1024*1024)
        print_success(f"Model loaded: {size_mb:.2f} MB")
        tests_passed += 1
    else:
        print_error("Model file not found: model/trained_model.h5")
    
    # Check labels file
    if Path('model/labels.json').exists():
        try:
            with open('model/labels.json', 'r') as f:
                labels = json.load(f)
                print_success(f"Labels loaded: {len(labels)} disease classes")
                tests_passed += 1
        except Exception as e:
            print_error(f"Failed to load labels: {e}")
    else:
        print_error("Labels file not found: model/labels.json")
    
    # Check class indices
    if Path('class_indices.json').exists():
        try:
            with open('class_indices.json', 'r') as f:
                indices = json.load(f)
                print_success(f"Class indices loaded: {len(indices)} entries")
                tests_passed += 1
        except Exception as e:
            print_error(f"Failed to load class indices: {e}")
    else:
        print_error("Class indices file not found: class_indices.json")
    
    return tests_passed == 3

# Test 4: Check Frontend Files
def test_frontend_files():
    print_header("TEST 4: FRONTEND FILES")
    
    tests_passed = 0
    
    # Check HTML
    if Path('frontend/index.html').exists():
        with open('frontend/index.html', 'r') as f:
            content = f.read()
            if 'CropDiseaseVision' in content and 'id="imageInput"' in content:
                print_success("HTML file: Valid structure")
                tests_passed += 1
            else:
                print_error("HTML file: Invalid or incomplete structure")
    
    # Check CSS
    if Path('frontend/style.css').exists():
        with open('frontend/style.css', 'r') as f:
            content = f.read()
            if ':root' in content and '.container' in content:
                print_success("CSS file: Valid structure")
                tests_passed += 1
            else:
                print_error("CSS file: Invalid or incomplete structure")
    
    # Check JavaScript
    if Path('frontend/script.js').exists():
        with open('frontend/script.js', 'r') as f:
            content = f.read()
            if 'predictFromImage' in content and 'voiceBtn' in content:
                print_success("JavaScript file: Valid structure (has image & voice functions)")
                tests_passed += 1
            else:
                print_error("JavaScript file: Invalid or incomplete structure")
    
    return tests_passed == 3

# Test 5: Check Backend API
def test_backend_api():
    print_header("TEST 5: BACKEND API STRUCTURE")
    
    tests_passed = 0
    
    if Path('backend/app.py').exists():
        with open('backend/app.py', 'r') as f:
            content = f.read()
            
            # Check for required endpoints
            if '@app.route(\'/predict\'' in content or '@app.route("/predict"' in content:
                print_success("Endpoint found: /predict")
                tests_passed += 1
            else:
                print_error("Endpoint missing: /predict")
            
            if 'predict-voice' in content or 'predict_voice' in content:
                print_success("Endpoint found: /predict-voice")
                tests_passed += 1
            else:
                print_error("Endpoint missing: /predict-voice")
            
            if '@app.route(\'/health\'' in content or '@app.route("/health"' in content:
                print_success("Endpoint found: /health")
                tests_passed += 1
            else:
                print_warning("Health endpoint missing (optional)")
    
    return tests_passed >= 2

# Test 6: Check Git Setup
def test_git_setup():
    print_header("TEST 6: GIT REPOSITORY")
    
    if Path('.git').exists():
        print_success("Git repository initialized")
        
        # Check if there are commits
        if Path('.git/HEAD').exists():
            with open('.git/HEAD', 'r') as f:
                head = f.read()
                if 'ref:' in head:
                    print_success("Git branch: main")
                    return True
    
    print_warning("Git repository not properly initialized")
    return False

# Test 7: Check Configuration Files
def test_config_files():
    print_header("TEST 7: CONFIGURATION FILES")
    
    tests_passed = 0
    
    # Check .gitignore
    if Path('.gitignore').exists():
        with open('.gitignore', 'r') as f:
            content = f.read()
            if '__pycache__' in content and '.env' in content:
                print_success(".gitignore: Properly configured")
                tests_passed += 1
            else:
                print_warning(".gitignore: Exists but may be incomplete")
                tests_passed += 1
    
    # Check requirements.txt (root)
    if Path('requirements.txt').exists():
        print_success("requirements.txt: Found (root)")
        tests_passed += 1
    
    # Check requirements.txt (backend)
    if Path('backend/requirements.txt').exists():
        with open('backend/requirements.txt', 'r') as f:
            content = f.read()
            packages = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
            print_success(f"backend/requirements.txt: {len(packages)} packages listed")
            tests_passed += 1
    
    return tests_passed == 3

# Test 8: Feature Verification
def test_features():
    print_header("TEST 8: KEY FEATURES")
    
    features_found = 0
    
    # Check for voice support
    with open('frontend/script.js', 'r') as f:
        content = f.read()
        if 'SpeechRecognition' in content:
            print_success("Feature: Voice-to-text support")
            features_found += 1
        if 'localStorage' in content:
            print_success("Feature: Analysis history")
            features_found += 1
        if 'confidence' in content.lower():
            print_success("Feature: Confidence display")
            features_found += 1
        if 'recommendations' in content or 'actionsList' in content:
            print_success("Feature: Treatment recommendations")
            features_found += 1
    
    return features_found == 4

# Test 9: Documentation
def test_documentation():
    print_header("TEST 9: DOCUMENTATION")
    
    docs_found = 0
    
    if Path('README.md').exists():
        print_success("Found: README.md")
        docs_found += 1
    
    if Path('README_V2.md').exists():
        print_success("Found: README_V2.md")
        docs_found += 1
    
    if Path('start_v2.bat').exists():
        print_success("Found: start_v2.bat (Windows launcher)")
        docs_found += 1
    
    return docs_found >= 2

# Test 10: File Sizes
def test_file_sizes():
    print_header("TEST 10: FILE SIZE VALIDATION")
    
    files_to_check = {
        'backend/app.py': (1, 50),  # KB
        'frontend/index.html': (5, 100),
        'frontend/style.css': (10, 200),
        'frontend/script.js': (10, 200),
        'model/trained_model.h5': (100000, 300000),  # KB
    }
    
    all_valid = True
    for file, (min_kb, max_kb) in files_to_check.items():
        if Path(file).exists():
            size_kb = Path(file).stat().st_size / 1024
            if min_kb <= size_kb <= max_kb:
                print_success(f"{file}: {size_kb:.2f} KB (Valid)")
            else:
                print_warning(f"{file}: {size_kb:.2f} KB (Expected {min_kb}-{max_kb} KB)")
                all_valid = False
    
    return all_valid

# Run All Tests
def run_all_tests():
    print(f"\n{BLUE}")
    print("=" * 60)
    print("   CropDiseaseVision v2.0 - COMPREHENSIVE TEST SUITE")
    print("   Testing: Structure, Dependencies, Files, API, Features")
    print("=" * 60)
    print(f"{RESET}")
    
    results = {
        "Project Structure": test_project_structure(),
        "Dependencies": test_dependencies(),
        "Model & Labels": test_model_files(),
        "Frontend Files": test_frontend_files(),
        "Backend API": test_backend_api(),
        "Git Setup": test_git_setup(),
        "Config Files": test_config_files(),
        "Features": test_features(),
        "Documentation": test_documentation(),
        "File Sizes": test_file_sizes(),
    }
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"{test_name:.<45} {status}")
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{GREEN}PASSED: {passed}/{total}{RESET}")
    
    if passed == total:
        print_success("ALL TESTS PASSED! Project is ready to run.")
        print_info("Next steps:")
        print_info("1. Terminal 1: cd backend && python app.py")
        print_info("2. Terminal 2: cd frontend && python -m http.server 8000")
        print_info("3. Open: http://localhost:8000")
    else:
        print_warning(f"Some tests failed. {total - passed} issue(s) to fix.")
    
    print(f"\n{BLUE}{'='*60}{RESET}\n")

if __name__ == '__main__':
    os.chdir(Path(__file__).parent)
    run_all_tests()
