from pathlib import Path
from collections import Counter
import yaml

# ============================================================
# CONFIGURATION
# ============================================================

# Change this to the root folder containing:
# images/
# labels/
# data.yaml
DATASET_ROOT = Path(r"C:\Users\User\Documents\final_year_project\datasets\august_combined_dataset\august_surveillance_dataset")

IMAGES_DIR = DATASET_ROOT / "images"
LABELS_DIR = DATASET_ROOT / "labels"
YAML_FILE = DATASET_ROOT / "data.yaml"


# ============================================================
# LOAD CLASS NAMES FROM data.yaml
# ============================================================

with open(YAML_FILE, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

names = data.get("names")

# Handle both formats:
#
# names:
#   0: person
#   1: masked
#
# OR:
#
# names: [person, masked]

if isinstance(names, dict):
    class_names = {
        int(k): v for k, v in names.items()
    }

elif isinstance(names, list):
    class_names = {
        i: name for i, name in enumerate(names)
    }

else:
    raise ValueError(
        "Could not find a valid 'names' section in data.yaml"
    )


# ============================================================
# FIND ALL IMAGES AND LABEL FILES
# ============================================================

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png",
    ".bmp", ".webp"
}

image_files = [
    f for f in IMAGES_DIR.rglob("*")
    if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
]

label_files = list(LABELS_DIR.rglob("*.txt"))


# ============================================================
# COUNT CLASS INSTANCES
# ============================================================

instance_counts = Counter()
invalid_class_ids = Counter()
total_instances = 0
empty_label_files = 0

for label_file in label_files:

    with open(label_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        empty_label_files += 1
        continue

    for line_number, line in enumerate(lines, start=1):

        line = line.strip()

        if not line:
            continue

        parts = line.split()

        # YOLO detection format:
        # class_id x_center y_center width height
        if len(parts) < 5:
            print(
                f"WARNING: Invalid annotation in:\n"
                f"{label_file}\n"
                f"Line {line_number}: {line}\n"
            )
            continue

        try:
            class_id = int(float(parts[0]))
        except ValueError:
            print(
                f"WARNING: Invalid class ID in:\n"
                f"{label_file}\n"
                f"Line {line_number}: {line}\n"
            )
            continue

        if class_id in class_names:
            instance_counts[class_id] += 1
        else:
            invalid_class_ids[class_id] += 1

        total_instances += 1


# ============================================================
# CHECK IMAGE/LABEL MATCHING
# ============================================================

image_stems = {
    image.relative_to(IMAGES_DIR).with_suffix("")
    for image in image_files
}

label_stems = {
    label.relative_to(LABELS_DIR).with_suffix("")
    for label in label_files
}

images_without_labels = image_stems - label_stems
labels_without_images = label_stems - image_stems


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("DATASET INSTANCE COUNT")
print("=" * 60)

print(f"\nDataset root: {DATASET_ROOT}")
print(f"Images found: {len(image_files)}")
print(f"Label files found: {len(label_files)}")
print(f"Empty label files: {empty_label_files}")

print("\n" + "-" * 60)
print("INSTANCES PER CLASS")
print("-" * 60)

for class_id in sorted(class_names):

    class_name = class_names[class_id]
    count = instance_counts[class_id]

    print(
        f"Class {class_id}: "
        f"{class_name:<20} = {count:,} instances"
    )


print("\n" + "-" * 60)
print(f"TOTAL VALID INSTANCES: {sum(instance_counts.values()):,}")
print("-" * 60)


# ============================================================
# INVALID CLASS IDs
# ============================================================

if invalid_class_ids:

    print("\nWARNING: CLASS IDs NOT FOUND IN data.yaml")

    for class_id, count in sorted(invalid_class_ids.items()):
        print(
            f"Class ID {class_id}: "
            f"{count:,} instances"
        )


# ============================================================
# IMAGE / LABEL MISMATCHES
# ============================================================

print("\n" + "-" * 60)
print("IMAGE / LABEL CHECK")
print("-" * 60)

print(
    f"Images without corresponding labels: "
    f"{len(images_without_labels)}"
)

print(
    f"Labels without corresponding images: "
    f"{len(labels_without_images)}"
)


# ============================================================
# SHOW SOME MISSING FILES
# ============================================================

if images_without_labels:

    print("\nFirst 10 images without labels:")

    for item in sorted(images_without_labels)[:10]:
        print(item)


if labels_without_images:

    print("\nFirst 10 labels without images:")

    for item in sorted(labels_without_images)[:10]:
        print(item)


print("\n" + "=" * 60)
print("DONE")
print("=" * 60)