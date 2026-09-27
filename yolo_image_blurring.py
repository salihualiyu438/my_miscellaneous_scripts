import os
import cv2
import numpy as np

# =========================
# CONFIGURATION
# =========================

image_dir = r"C:\Users\User\Documents\final_year_project\datasets\Arm Detection\train\images"
label_dir = r"C:\Users\User\Documents\final_year_project\datasets\Arm Detection\train\labels"
TARGET_CLASS = 2

# Blur strength (must be odd)
BLUR_KERNEL = (201, 201)

# Output folder
output_dir = f"blurred_{os.path.basename(image_dir)}"

os.makedirs(output_dir, exist_ok=True)

# Supported image extensions
image_extensions = [".jpg", ".jpeg", ".png", ".bmp"]

# =========================
# PROCESSING
# =========================

for label_file in os.listdir(label_dir):

    if not label_file.endswith(".txt"):
        continue

    label_path = os.path.join(label_dir, label_file)

    # Find corresponding image
    base_name = os.path.splitext(label_file)[0]

    image_path = None

    for ext in image_extensions:

        candidate = os.path.join(image_dir, base_name + ext)

        if os.path.exists(candidate):
            image_path = candidate
            break

    # Skip if image not found
    if image_path is None:
        print(f"Image not found for: {label_file}")
        continue

    # Read image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Failed to load image: {image_path}")
        continue

    h, w = image.shape[:2]

    # Create mask for class 1 regions
    mask = np.zeros((h, w), dtype=np.uint8)

    found_target = False

    with open(label_path, "r") as f:

        lines = f.readlines()

        for line in lines:

            parts = line.strip().split()

            if len(parts) != 5:
                continue

            cls_id = int(float(parts[0]))

            if cls_id != TARGET_CLASS:
                continue

            found_target = True

            xc = float(parts[1])
            yc = float(parts[2])
            bw = float(parts[3])
            bh = float(parts[4])

            # Convert YOLO coords to pixel coords
            x1 = int((xc - bw / 2) * w)
            y1 = int((yc - bh / 2) * h)

            x2 = int((xc + bw / 2) * w)
            y2 = int((yc + bh / 2) * h)

            # Clamp coordinates
            x1 = max(0, x1)
            y1 = max(0, y1)

            x2 = min(w, x2)
            y2 = min(h, y2)

            # Draw white rectangle on mask
            mask[y1:y2, x1:x2] = 255

    # Skip images without class 1
    if not found_target:
        continue

    # Create blurred version
    blurred = cv2.GaussianBlur(image, BLUR_KERNEL, 0)

    # Keep original inside mask
    result = np.where(mask[:, :, np.newaxis] == 255, image, blurred)

    # Save result
    output_path = os.path.join(output_dir, os.path.basename(image_path))

    cv2.imwrite(output_path, result)

    print(f"Saved: {output_path}")

print("Processing complete.")