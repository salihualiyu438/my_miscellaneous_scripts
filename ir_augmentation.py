from pathlib import Path
from collections import Counter
import random
import shutil

import cv2
import numpy as np
import yaml


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_ROOT = Path(
    r"C:\Users\User\Documents\final_year_project\datasets"
    r"\september_dataset\WEAPON DETECTOR\resized_dataset"
)

DATA_YAML = DATASET_ROOT / "data.yaml"

IMAGES_DIR = DATASET_ROOT / "images"
LABELS_DIR = DATASET_ROOT / "labels"

# ------------------------------------------------------------
# Which dataset splits should receive IR augmentation?
#
# Recommended:
# train = True
# val   = False
# ------------------------------------------------------------

AUGMENT_TRAIN = True
AUGMENT_VAL = True


# ------------------------------------------------------------
# Classes whose images should receive an IR duplicate
# ------------------------------------------------------------

TARGET_CLASSES = {
    "large_gun",
    "short_gun",
    "matchet/knife"
}


# ------------------------------------------------------------
# Random seed
# ------------------------------------------------------------

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# ------------------------------------------------------------
# Output suffix
# ------------------------------------------------------------

IR_SUFFIX = "_ir_aug"


# ============================================================
# LOAD DATA.YAML
# ============================================================

print("=" * 70)
print("LOADING DATASET")
print("=" * 70)

with open(DATA_YAML, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

names = data["names"]

if isinstance(names, dict):
    CLASS_NAMES = {
        int(k): str(v)
        for k, v in names.items()
    }
else:
    CLASS_NAMES = {
        i: str(v)
        for i, v in enumerate(names)
    }

NAME_TO_ID = {
    name: class_id
    for class_id, name in CLASS_NAMES.items()
}


print("\nClasses found in data.yaml:")

for class_id in sorted(CLASS_NAMES):
    print(f"  {class_id}: {CLASS_NAMES[class_id]}")


# ============================================================
# CHECK TARGET CLASSES
# ============================================================

print("\n" + "-" * 70)
print("TARGET CLASSES")
print("-" * 70)

TARGET_CLASS_IDS = set()

for class_name in TARGET_CLASSES:

    if class_name not in NAME_TO_ID:
        print(
            f"WARNING: '{class_name}' was not found "
            f"in data.yaml"
        )
    else:
        class_id = NAME_TO_ID[class_name]
        TARGET_CLASS_IDS.add(class_id)

        print(
            f"  {class_name} -> class ID {class_id}"
        )


if not TARGET_CLASS_IDS:
    raise RuntimeError(
        "None of the TARGET_CLASSES were found in data.yaml."
    )


# ============================================================
# IR IMAGE GENERATOR
# ============================================================

def create_ir_image(image):
    """
    Convert an RGB/BGR surveillance image into a
    randomized synthetic IR/night-vision-style image.

    The original image is NOT modified.
    """

    # --------------------------------------------------------
    # 1. Convert to grayscale
    # --------------------------------------------------------

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # --------------------------------------------------------
    # 2. Random gamma adjustment
    # --------------------------------------------------------

    gamma = random.uniform(0.65, 1.35)

    normalized = gray.astype(np.float32) / 255.0

    corrected = np.power(normalized, gamma)

    gray = np.clip(
        corrected * 255,
        0,
        255
    ).astype(np.uint8)

    # --------------------------------------------------------
    # 3. CLAHE / local contrast
    # --------------------------------------------------------

    clip_limit = random.uniform(1.5, 3.5)

    tile_size = random.choice([6, 8, 10])

    clahe = cv2.createCLAHE(
        clipLimit=clip_limit,
        tileGridSize=(tile_size, tile_size)
    )

    gray = clahe.apply(gray)

    # --------------------------------------------------------
    # 4. Optional slight blur
    # --------------------------------------------------------

    if random.random() < 0.45:

        kernel_size = random.choice([3, 5])

        gray = cv2.GaussianBlur(
            gray,
            (kernel_size, kernel_size),
            0
        )

    # --------------------------------------------------------
    # 5. IR sensor noise
    # --------------------------------------------------------

    noise_strength = random.uniform(2.0, 9.0)

    noise = np.random.normal(
        0,
        noise_strength,
        gray.shape
    )

    noisy = gray.astype(np.float32) + noise

    gray = np.clip(
        noisy,
        0,
        255
    ).astype(np.uint8)

    # --------------------------------------------------------
    # 6. Random contrast / brightness
    # --------------------------------------------------------

    alpha = random.uniform(0.85, 1.30)
    beta = random.uniform(-25, 20)

    gray = cv2.convertScaleAbs(
        gray,
        alpha=alpha,
        beta=beta
    )

    # --------------------------------------------------------
    # 7. Choose IR presentation
    #
    # Some IR cameras appear almost monochrome.
    # Others have a slight green/blue tint.
    # --------------------------------------------------------

    style = random.choice([
        "grayscale",
        "green",
        "blue",
        "white_hot"
    ])

    if style == "grayscale":

        result = cv2.cvtColor(
            gray,
            cv2.COLOR_GRAY2BGR
        )

    elif style == "green":

        result = np.zeros(
            (gray.shape[0], gray.shape[1], 3),
            dtype=np.uint8
        )

        result[:, :, 1] = gray

        # Small amount of red/blue channel information
        result[:, :, 0] = (
            gray.astype(np.float32) * 0.12
        ).astype(np.uint8)

        result[:, :, 2] = (
            gray.astype(np.float32) * 0.05
        ).astype(np.uint8)

    elif style == "blue":

        result = np.zeros(
            (gray.shape[0], gray.shape[1], 3),
            dtype=np.uint8
        )

        result[:, :, 0] = gray

        result[:, :, 1] = (
            gray.astype(np.float32) * 0.25
        ).astype(np.uint8)

    else:
        # White-hot style
        result = cv2.cvtColor(
            gray,
            cv2.COLOR_GRAY2BGR
        )

    # --------------------------------------------------------
    # 8. Optional slight vignette
    # --------------------------------------------------------

    if random.random() < 0.30:

        h, w = gray.shape

        y, x = np.ogrid[:h, :w]

        center_x = w / 2
        center_y = h / 2

        distance = np.sqrt(
            ((x - center_x) / center_x) ** 2 +
            ((y - center_y) / center_y) ** 2
        )

        vignette = 1 - np.clip(
            distance * random.uniform(0.05, 0.18),
            0,
            0.25
        )

        result = (
            result.astype(np.float32)
            * vignette[:, :, None]
        )

        result = np.clip(
            result,
            0,
            255
        ).astype(np.uint8)

    return result


# ============================================================
# PROCESS ONE DATASET SPLIT
# ============================================================

def process_split(split_name):

    images_dir = IMAGES_DIR / split_name
    labels_dir = LABELS_DIR / split_name

    if not images_dir.exists():

        print(
            f"\nWARNING: Images directory does not exist:"
        )
        print(images_dir)

        return {
            "images": 0,
            "qualifying": 0,
            "generated": 0,
            "skipped": 0,
            "class_counts": Counter()
        }

    if not labels_dir.exists():

        print(
            f"\nWARNING: Labels directory does not exist:"
        )
        print(labels_dir)

        return {
            "images": 0,
            "qualifying": 0,
            "generated": 0,
            "skipped": 0,
            "class_counts": Counter()
        }

    image_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".webp"
    }

    image_files = [
        p for p in images_dir.rglob("*")
        if p.is_file()
        and p.suffix.lower() in image_extensions
    ]

    total_images = len(image_files)

    qualifying_images = 0
    generated_images = 0
    skipped_images = 0

    class_counts = Counter()

    print("\n" + "=" * 70)
    print(f"PROCESSING: {split_name.upper()}")
    print("=" * 70)

    print(f"Images found: {total_images}")

    for index, image_path in enumerate(image_files, start=1):

        # ----------------------------------------------------
        # Find corresponding label
        # ----------------------------------------------------

        relative_path = image_path.relative_to(images_dir)

        label_path = (
            labels_dir
            / relative_path.with_suffix(".txt")
        )

        if not label_path.exists():

            skipped_images += 1

            continue

        # ----------------------------------------------------
        # Read YOLO annotation
        # ----------------------------------------------------

        try:

            with open(
                label_path,
                "r",
                encoding="utf-8"
            ) as f:

                lines = [
                    line.strip()
                    for line in f
                    if line.strip()
                ]

        except Exception as e:

            print(
                f"\nWARNING: Could not read label:"
            )
            print(label_path)
            print(e)

            skipped_images += 1

            continue

        # ----------------------------------------------------
        # Extract class IDs
        # ----------------------------------------------------

        image_class_ids = set()

        for line in lines:

            parts = line.split()

            if not parts:
                continue

            try:
                class_id = int(float(parts[0]))
            except ValueError:
                continue

            image_class_ids.add(class_id)

        # ----------------------------------------------------
        # Determine whether image qualifies
        # ----------------------------------------------------

        matching_classes = (
            image_class_ids & TARGET_CLASS_IDS
        )

        if not matching_classes:
            continue

        qualifying_images += 1

        # Count image occurrences for each target class
        for class_id in matching_classes:
            class_counts[class_id] += 1

        # ----------------------------------------------------
        # Generate IR filename
        # ----------------------------------------------------

        new_stem = (
            image_path.stem
            + IR_SUFFIX
        )

        new_image_path = (
            image_path.parent
            / (new_stem + image_path.suffix)
        )

        new_label_path = (
            label_path.parent
            / (new_stem + ".txt")
        )

        # ----------------------------------------------------
        # Don't overwrite existing IR images
        # ----------------------------------------------------

        if new_image_path.exists():

            print(
                f"\nSKIPPED - IR image already exists:"
            )
            print(new_image_path)

            skipped_images += 1

            continue

        # ----------------------------------------------------
        # Read image
        # ----------------------------------------------------

        image = cv2.imread(
            str(image_path),
            cv2.IMREAD_COLOR
        )

        if image is None:

            print(
                f"\nWARNING: Could not read image:"
            )
            print(image_path)

            skipped_images += 1

            continue

        # ----------------------------------------------------
        # Create IR version
        # ----------------------------------------------------

        ir_image = create_ir_image(image)

        # ----------------------------------------------------
        # Save IR image
        # ----------------------------------------------------

        success = cv2.imwrite(
            str(new_image_path),
            ir_image,
            [
                cv2.IMWRITE_JPEG_QUALITY,
                95
            ]
        )

        if not success:

            print(
                f"\nERROR: Could not save:"
            )
            print(new_image_path)

            skipped_images += 1

            continue

        # ----------------------------------------------------
        # Copy YOLO annotation
        # ----------------------------------------------------

        try:

            shutil.copy2(
                label_path,
                new_label_path
            )

        except Exception as e:

            print(
                f"\nERROR copying label:"
            )
            print(label_path)
            print(e)

            # Remove IR image because its label failed
            try:
                new_image_path.unlink()
            except:
                pass

            skipped_images += 1

            continue

        generated_images += 1

        # ----------------------------------------------------
        # Progress
        # ----------------------------------------------------

        if generated_images % 100 == 0:

            print(
                f"Progress: "
                f"{index}/{total_images} | "
                f"IR generated: {generated_images}"
            )

    return {
        "images": total_images,
        "qualifying": qualifying_images,
        "generated": generated_images,
        "skipped": skipped_images,
        "class_counts": class_counts
    }


# ============================================================
# RUN
# ============================================================

train_results = None
val_results = None


if AUGMENT_TRAIN:
    train_results = process_split("train")


if AUGMENT_VAL:
    val_results = process_split("val")


# ============================================================
# FINAL REPORT
# ============================================================

print("\n\n")
print("=" * 70)
print("IR AUGMENTATION COMPLETE")
print("=" * 70)


def print_results(split_name, results):

    if results is None:
        return

    print(f"\n{split_name.upper()}")
    print("-" * 70)

    print(
        f"Original images:             "
        f"{results['images']:,}"
    )

    print(
        f"Images containing targets:   "
        f"{results['qualifying']:,}"
    )

    print(
        f"IR images generated:         "
        f"{results['generated']:,}"
    )

    print(
        f"Images skipped/errors:       "
        f"{results['skipped']:,}"
    )

    print("\nImages containing each target class:")

    for class_id in sorted(
        results["class_counts"]
    ):

        class_name = CLASS_NAMES[class_id]

        count = results["class_counts"][class_id]

        print(
            f"  {class_name:<20} "
            f"{count:,} images"
        )


print_results("train", train_results)
print_results("val", val_results)


print("\n" + "=" * 70)
print("TARGET CLASSES")
print("=" * 70)

for class_name in TARGET_CLASSES:
    print(f"  {class_name}")

print("\nDone.")