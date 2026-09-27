import os
import shutil

# ============================================================
# CONFIGURATION
# ============================================================

# Original dataset
IMAGE_DIR = r"C:\Users\User\Documents\final_year_project\datasets\august_dataset\august_security_personnels_images"
LABEL_DIR = r"C:\Users\User\Documents\final_year_project\datasets\august_dataset\august_security_personnels_annotations"
# New extracted dataset
OUTPUT_IMAGE_DIR = r"C:\Users\User\Documents\final_year_project\datasets\september_dataset\HUMAN DETECTOR\images"
OUTPUT_LABEL_DIR = r"C:\Users\User\Documents\final_year_project\datasets\september_dataset\HUMAN DETECTOR\labels"

# Classes to extract
TARGET_CLASSES = {0, 3, 4, 5}

# Class names for information only
CLASS_NAMES = {
    0: "person",
    3: "animal",
    4: "vehicle",
    5: "personnel"
}


# ============================================================
# CREATE OUTPUT DIRECTORIES
# ============================================================

os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)
os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)


# ============================================================
# SUPPORTED IMAGE EXTENSIONS
# ============================================================

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


# ============================================================
# STATISTICS
# ============================================================

images_copied = 0
annotations_created = 0
class_counts = {
    0: 0,
    3: 0,
    4: 0,
    5: 0
}


# ============================================================
# PROCESS LABEL FILES
# ============================================================

for label_filename in os.listdir(LABEL_DIR):

    if not label_filename.lower().endswith(".txt"):
        continue

    label_path = os.path.join(LABEL_DIR, label_filename)

    # Read annotation
    with open(label_path, "r") as f:
        lines = f.readlines()

    selected_lines = []

    # --------------------------------------------------------
    # Check every annotation in this file
    # --------------------------------------------------------

    for line in lines:

        line = line.strip()

        if not line:
            continue

        parts = line.split()

        if len(parts) < 5:
            continue

        try:
            class_id = int(parts[0])
        except ValueError:
            continue

        # Keep only heavy_gun, matchet and small_gun
        if class_id in TARGET_CLASSES:

            selected_lines.append(line)

            class_counts[class_id] += 1

    # --------------------------------------------------------
    # If this image contains none of the target classes,
    # skip it completely.
    # --------------------------------------------------------

    if not selected_lines:
        continue

    # ========================================================
    # FIND CORRESPONDING IMAGE
    # ========================================================

    base_name = os.path.splitext(label_filename)[0]

    image_path = None

    for ext in IMAGE_EXTENSIONS:

        candidate = os.path.join(
            IMAGE_DIR,
            base_name + ext
        )

        if os.path.exists(candidate):
            image_path = candidate
            break

    # If image doesn't exist, skip
    if image_path is None:

        print(
            f"[WARNING] Image not found for: {label_filename}"
        )

        continue

    # ========================================================
    # COPY IMAGE
    # ========================================================

    output_image_path = os.path.join(
        OUTPUT_IMAGE_DIR,
        os.path.basename(image_path)
    )

    shutil.copy2(
        image_path,
        output_image_path
    )

    # ========================================================
    # CREATE NEW LABEL FILE
    # ========================================================

    output_label_path = os.path.join(
        OUTPUT_LABEL_DIR,
        label_filename
    )

    with open(output_label_path, "w") as f:

        for line in selected_lines:
            f.write(line + "\n")

    images_copied += 1
    annotations_created += 1

    print(
        f"[COPIED] {os.path.basename(image_path)}"
    )


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("EXTRACTION COMPLETE")
print("=" * 60)

print(f"Images copied       : {images_copied}")
print(f"Annotations created : {annotations_created}")

print("\nClass instances extracted:")

for class_id in TARGET_CLASSES:

    print(
        f"  {class_id} - "
        f"{CLASS_NAMES[class_id]}: "
        f"{class_counts[class_id]}"
    )

print("\nOutput:")
print(f"Images: {OUTPUT_IMAGE_DIR}")
print(f"Labels: {OUTPUT_LABEL_DIR}")

print("=" * 60)