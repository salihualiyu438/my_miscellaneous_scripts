import os
import cv2
import shutil

# ===== CONFIGURATION =====
INPUT_IMAGES_DIR = "dataset/images/train"
INPUT_LABELS_DIR = "dataset/labels/train"

OUTPUT_IMAGES_DIR = "dataset_optimized/images/train"
OUTPUT_LABELS_DIR = "dataset_optimized/labels/train"

IMG_HEIGHT = 1280
IMG_WIDTH = 720
JPEG_QUALITY = 85

# Create output directories
os.makedirs(OUTPUT_IMAGES_DIR, exist_ok=True)
os.makedirs(OUTPUT_LABELS_DIR, exist_ok=True)

# Supported image formats
image_extensions = [".jpg", ".jpeg", ".png"]

# ===== PROCESSING =====
for filename in os.listdir(INPUT_IMAGES_DIR):
    name, ext = os.path.splitext(filename)

    if ext.lower() not in image_extensions:
        continue

    img_path = os.path.join(INPUT_IMAGES_DIR, filename)
    label_path = os.path.join(INPUT_LABELS_DIR, name + ".txt")

    # Read image
    img = cv2.imread(img_path)
    if img is None:
        print(f"Skipping unreadable image: {filename}")
        continue

    # Resize image
    resized_img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

    # Save compressed image
    output_img_path = os.path.join(OUTPUT_IMAGES_DIR, name + ".jpg")
    cv2.imwrite(output_img_path, resized_img,
                [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])

    # Copy label file (if exists)
    if os.path.exists(label_path):
        shutil.copy(label_path, os.path.join(OUTPUT_LABELS_DIR, name + ".txt"))
    else:
        print(f"Warning: No label found for {filename}")

print(" Dataset optimization complete!")