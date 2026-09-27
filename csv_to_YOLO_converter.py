import os
import pandas as pd
from PIL import Image

# Path to your dataset
csv_file = "C:/Users/User/Downloads/archive/train/train/_annotations.csv"   # your CSV file
images_dir = "C:/Users/User/Downloads/archive/train/train"         # folder containing images
labels_dir = "C:/Users/User/Downloads/archive/train/train_annotations"         # folder to save YOLO txt files

os.makedirs(labels_dir, exist_ok=True)

# Load CSV
df = pd.read_csv(csv_file)

# Expected CSV columns: filename, xmin, ymin, xmax, ymax, class
for _, row in df.iterrows():
    image_path = os.path.join(images_dir, row['filename'])
    label_path = os.path.join(labels_dir, os.path.splitext(row['filename'])[0] + ".txt")

    # Get image size
    with Image.open(image_path) as img:
        img_w, img_h = img.size

    # Convert to YOLO format
    x_center = ((row['xmin'] + row['xmax']) / 2) / img_w
    y_center = ((row['ymin'] + row['ymax']) / 2) / img_h
    width = (row['xmax'] - row['xmin']) / img_w
    height = (row['ymax'] - row['ymin']) / img_h

    # Write to txt file
    with open(label_path, "a") as f:  # "a" allows multiple boxes per image
        f.write(f"{row['class']} {x_center} {y_center} {width} {height}\n")

print("✅ Conversion complete! YOLO txt files saved in:", labels_dir)
