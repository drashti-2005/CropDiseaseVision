import os
import subprocess
import sys
import zipfile
import shutil

def main():
    print("🌾 Crop Disease Dataset Downloader")
    print("-----------------------------------")
    print("This script uses Kaggle to download the 'PlantVillage' dataset.")
    print("Note: You need a Kaggle account and an API token (kaggle.json) setup.\n")
    
    # Check if kaggle is installed, install if not
    try:
        import kaggle
    except ImportError:
        print("📦 'kaggle' Python library not found. Installing it now...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
            print("✅ 'kaggle' installed successfully!")
        except Exception as e:
            print(f"❌ Failed to install kaggle: {e}")
            return
            
        print("\n⚠️ ACTION REQUIRED:")
        print("1. Go to Kaggle.com -> Account Settings -> Create New APi Token (downloads a kaggle.json file).")
        print("2. Place the 'kaggle.json' file in your Kaggle configuration directory:")
        print("   - Windows: C:\\Users\\<YourUsername>\\.kaggle\\kaggle.json")
        print("   - Mac/Linux: ~/.kaggle/kaggle.json")
        print("3. Run this script again!\n")
        return

    # Dataset to download
    # 'abdallahalidev/plantvillage-dataset' contains clean disease category folders.
    dataset_name = "abdallahalidev/plantvillage-dataset"
    target_dir = os.path.join(os.path.dirname(__file__), "dataset")
    zip_filename = "plantvillage-dataset.zip"
    
    os.makedirs(target_dir, exist_ok=True)
    print(f"⏳ Downloading dataset '{dataset_name}' into '{target_dir}'...")
    
    try:
        # Download from kaggle
        subprocess.check_call(["kaggle", "datasets", "download", "-d", dataset_name, "-p", target_dir])
        
        zip_path = os.path.join(target_dir, zip_filename)
        if os.path.exists(zip_path):
            print("⏳ Extracting dataset... (This might take a few minutes as it contains ~54,000 images)")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(target_dir)
            
            print("🧹 Cleaning up zip file...")
            os.remove(zip_path)
            
            # The dataset usually extracts into a subfolder like "plantvillage dataset/color/"
            # We want the disease folders directly inside our "dataset" folder to work with our code.
            # Let's see if we need to move them:
            extracted_subfolders = [f for f in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, f))]
            color_dir = os.path.join(target_dir, "plantvillage dataset", "color")
            
            if os.path.exists(color_dir):
                print("📂 Organizing folders to match our project structure...")
                for item in os.listdir(color_dir):
                    s = os.path.join(color_dir, item)
                    d = os.path.join(target_dir, item)
                    if not os.path.exists(d):
                        shutil.move(s, d)
                
                # Cleanup the empty parent folders
                shutil.rmtree(os.path.join(target_dir, "plantvillage dataset"), ignore_errors=True)
                shutil.rmtree(os.path.join(target_dir, "segmented"), ignore_errors=True)
                shutil.rmtree(os.path.join(target_dir, "grayscale"), ignore_errors=True)
        
            print("\n✅ Dataset successfully downloaded and prepared!")
            print("You can now train your real AI model by running:")
            print("python model/train.py")
        else:
            print("❌ Download completely but couldn't find the zip file.")
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Kaggle API Error. Have you set up your kaggle.json file correctly?")
        print("Please ensure your kaggle.json is in the correct directory (.kaggle) and run again.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
