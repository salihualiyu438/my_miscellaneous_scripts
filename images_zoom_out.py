import os
import cv2
import random

# ==========================================
# CONFIGURATION
# ==========================================

input_folder = r"C:\Users\User\Documents\final_year_project\datasets\selected\merged_datasets"
label_folder = r"C:\Users\User\Documents\final_year_project\datasets\selected\merged_datasets_annotations"

# Random zoom-out range
MIN_SCALE = 0.3
MAX_SCALE = 0.3

# Padding color (B, G, R)
PAD_COLOR = (20, 20, 0)

# ==========================================
# OUTPUT FOLDERS
# ==========================================

folder_name = os.path.basename(input_folder.rstrip("/\\"))
output_image_folder = f"zoomed_{folder_name}"

label_folder_name = os.path.basename(label_folder.rstrip("/\\"))
output_label_folder = f"zoomed_{label_folder_name}"

os.makedirs(output_image_folder, exist_ok=True)
os.makedirs(output_label_folder, exist_ok=True)

# ==========================================
# PROCESS IMAGES
# ==========================================

valid_exts = [".jpg", ".jpeg", ".png"]

for file in os.listdir(input_folder):

    ext = os.path.splitext(file)[1].lower()

    if ext not in valid_exts:
        continue

    image_path = os.path.join(input_folder, file)

    image = cv2.imread(image_path)

    if image is None:
        continue

    h, w = image.shape[:2]

    # --------------------------------------
    # RANDOM SCALE
    # --------------------------------------

    scale = random.uniform(MIN_SCALE, MAX_SCALE)

    new_w = int(w * scale)
    new_h = int(h * scale)

    resized = cv2.resize(image, (new_w, new_h))

    # --------------------------------------
    # CREATE PADDED CANVAS
    # --------------------------------------

    canvas = cv2.copyMakeBorder(
        resized,
        top=(h - new_h) // 2,
        bottom=h - new_h - ((h - new_h) // 2),
        left=(w - new_w) // 2,
        right=w - new_w - ((w - new_w) // 2),
        borderType=cv2.BORDER_CONSTANT,
        value=PAD_COLOR
    )

    # --------------------------------------
    # SAVE IMAGE
    # --------------------------------------

    output_image_path = os.path.join(output_image_folder, file)

    cv2.imwrite(output_image_path, canvas)

    # ======================================
    # PROCESS YOLO LABELS
    # ======================================

    label_file = os.path.splitext(file)[0] + ".txt"

    input_label_path = os.path.join(label_folder, label_file)

    output_label_path = os.path.join(output_label_folder, label_file)

    if not os.path.exists(input_label_path):
        continue

    updated_labels = []

    with open(input_label_path, "r") as f:
        lines = f.readlines()

    for line in lines:

        parts = line.strip().split()

        if len(parts) != 5:
            continue

        cls_id, x, y, bw, bh = parts

        x = float(x)
        y = float(y)
        bw = float(bw)
        bh = float(bh)

        # ----------------------------------
        # Adjust for scaling
        # ----------------------------------

        bw *= scale
        bh *= scale

        # Object center shifts because image
        # is centered inside padded canvas

        x = ((x * new_w) + ((w - new_w) / 2)) / w
        y = ((y * new_h) + ((h - new_h) / 2)) / h

        updated_labels.append(
            f"{cls_id} {x:.6f} {y:.6f} {bw:.6f} {bh:.6f}"
        )

    with open(output_label_path, "w") as f:
        f.write("\n".join(updated_labels))

print("Done.")