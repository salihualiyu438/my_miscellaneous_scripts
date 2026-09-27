from ultralytics import YOLO
import os

# ===== CONFIG =====
IMAGE_DIR = r"C:\Users\User\Documents\final_year_project\datasets\september_dataset\HUMAN DETECTOR\infra_record_extracted_uncompressed"      # folder with your images
OUTPUT_DIR = r"C:\Users\User\Documents\final_year_project\datasets\september_dataset\HUMAN DETECTOR\annot_infra_record_extracted_uncompressed" # output folder
MODEL_PATH = "yolov8x.pt"   # most accurate standard model

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===== LOAD MODEL =====
model = YOLO(MODEL_PATH)

# ===== CLASS MAPPING =====
# COCO class indices
PERSON = [0] # YOLO standard
PHONE = [67]
HEAD = [0]
MASKED = [1]
UNMASKED = [7]
HEAVY_GUN = [2]
SMALL_GUN = [8]
KNIFE = [0]
GUN = [1]
# VEHICLES = [2, 3, 5, 7]  # YOLO standard
VEHICLE = [4]
# car, motorcycle, bus, truck

ANIMALS = [15, 16, 17, 18, 19, 20, 21, 22, 23]  
# cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe

# Custom mapping
CLASS_MAP = {
    "person": 0,
    # "cell_phone": 5,
    # "vehicle": 4,
    # "animal": 3,
    # "head": 7,
    # "masked": 1,
    # "unmasked": 7,
    # "heavy_gun": 2,
    # "small_gun": 8,
    # "knife": 0,
    # "gun": 1
}
counter = 1
# ===== PROCESS IMAGES =====
for img_name in os.listdir(IMAGE_DIR):
    if not img_name.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    img_path = os.path.join(IMAGE_DIR, img_name)
    output_txt = os.path.join(OUTPUT_DIR, os.path.splitext(img_name)[0] + ".txt")

    if os.path.exists(output_txt):
        print('path already exists! Skipping...')
        continue
    results = model(img_path)[0]

    h, w = results.orig_shape

    
    lines = []

    for box in results.boxes:
        cls_id = int(box.cls[0])
        x1, y1, x2, y2 = box.xyxy[0]

        x_center = ((x1 + x2) / 2) / w
        y_center = ((y1 + y2) / 2) / h
        width = (x2 - x1) / w
        height = (y2 - y1) / h

        if cls_id in PERSON:
            new_class = CLASS_MAP["person"]
        # elif cls_id in VEHICLES:
        # #     new_class = CLASS_MAP["vehicle"]
        # elif cls_id in GUN:
        #     new_class = CLASS_MAP["gun"]

        # elif cls_id in HEAVY_GUN:
        #     new_class = CLASS_MAP["heavy_gun"]

        # elif cls_id in UNMASKED:
        #     new_class = CLASS_MAP["unmasked"]

        # elif cls_id in VEHICLE:
        #     new_class = CLASS_MAP["vehicle"]
        else:
            continue

        lines.append(f"{new_class} {x_center} {y_center} {width} {height}")

    with open(output_txt, "a") as f:
        if os.path.getsize(output_txt) > 0 and lines:
            f.write("\n")
        f.write("\n".join(lines))
    print(f"Processed:{counter} {img_name}")
    counter+=1

print("DONE!")