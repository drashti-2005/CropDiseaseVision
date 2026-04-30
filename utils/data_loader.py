import os
import random
import glob

def get_50_random_images(dataset_path, num_images=50):
    """
    Reads images from 'dataset_path' and returns exactly 'num_images' randomly 
    sampled across multiple classes.
    """
    # Find all images inside the subdirectories
    search_path = os.path.join(dataset_path, "*", "*.*")
    all_images = glob.glob(search_path)
    
    # Filter for common image extensions (handles spaces in paths correctly)
    valid_exts = ('.jpg', '.jpeg', '.png')
    all_images = [img for img in all_images if img.lower().endswith(valid_exts)]
    
    if len(all_images) < num_images:
        print(f"Warning: Only found {len(all_images)} images, requesting {num_images}")
        num_images = len(all_images)
        
    if num_images == 0:
        return [], []
        
    # Randomly sample exactly `num_images` from the dataset
    sampled_images = random.sample(all_images, num_images)
    
    paths = []
    labels = []
    
    for img_path in sampled_images:
        # The class label is the name of the folder containing the image
        folder_name = os.path.basename(os.path.dirname(img_path))
        paths.append(img_path)
        labels.append(folder_name)
        
    return paths, labels
