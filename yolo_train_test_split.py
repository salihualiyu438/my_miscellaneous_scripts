"""
split_dataset.py
────────────────
Stratified train/val/test split for a YOLO-format dataset.

Input structure (what you have now)
────────────────────────────────────
dataset/
├── images/
│   ├── img001.jpg
│   ├── img002.jpg
│   └── ...
└── labels/
    ├── img001.txt
    ├── img002.txt
    └── ...

Output structure (what this script creates)
────────────────────────────────────────────
dataset/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/

Stratification logic
────────────────────
Each image may contain multiple classes. This script assigns each image
a "primary class" — the class with the most instances in that image.
Images are then grouped by primary class and each group is split 80/10/10
independently, so every class is proportionally represented in all three
splits.

Images with no matching label file are collected separately and split
randomly (they are background / negative samples).

Usage
─────
1. Set DATASET_DIR to the path of your dataset folder.
2. Run:  python split_dataset.py
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import os
import shutil
import random
from collections import defaultdict, Counter
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# ▼▼▼  EDIT THIS  ▼▼▼
# ═══════════════════════════════════════════════════════════════

# Path to your dataset root folder
# (the folder that contains your images/ and labels/ subfolders)
DATASET_DIR = r"C:\Users\User\Documents\final_year_project\datasets\september_dataset\HUMAN DETECTOR\resized_dataset"
# Split ratios — must sum to 1.0
TRAIN_RATIO = 0.70
VAL_RATIO   = 0.20
TEST_RATIO  = 0.10

# Reproducibility — change or set to None for a different random split each run
RANDOM_SEED = 42

# Image extensions to look for
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# ═══════════════════════════════════════════════════════════════
# ▲▲▲  END OF CONFIG  ▲▲▲
# ═══════════════════════════════════════════════════════════════


def get_primary_class(label_path: Path) -> int | None:
    """
    Read a YOLO label file and return the class index that appears
    most frequently in it (the 'primary class' of this image).
    Returns None if the file is empty or missing.
    """
    if not label_path.exists():
        return None
    if label_path.name == "classes.txt":   # ← add this line
        return None
    classes = []
    try:
        with open(label_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    cls = int(line.split()[0])
                    classes.append(cls)
    except Exception:
        return None

    if not classes:
        return None

    # Most common class in this image
    return Counter(classes).most_common(1)[0][0]


def split_list(items: list, train_r: float, val_r: float, seed: int) -> tuple:
    """
    Randomly split a list into (train, val, test) subsets.
    test gets whatever is left after train and val.
    """
    rng = random.Random(seed)
    shuffled = items[:]
    rng.shuffle(shuffled)

    n        = len(shuffled)
    n_train  = max(1, round(n * train_r))          if n >= 3 else n
    n_val    = max(1, round(n * val_r))             if n >= 3 else 0
    # test gets the remainder
    n_train  = min(n_train, n)
    n_val    = min(n_val,   n - n_train)

    train = shuffled[:n_train]
    val   = shuffled[n_train : n_train + n_val]
    test  = shuffled[n_train + n_val :]

    return train, val, test


def copy_pair(stem: str, src_images: Path, src_labels: Path,
              dst_images: Path, dst_labels: Path,
              image_extensions: set) -> bool:
    """
    Copy one image + its label file to destination folders.
    Returns True if the image was found and copied.
    """
    # Find the image file (try all supported extensions)
    img_src = None
    for ext in image_extensions:
        candidate = src_images / (stem + ext)
        if candidate.exists():
            img_src = candidate
            break

    if img_src is None:
        print(f"  [WARN] No image found for stem '{stem}' — skipping.")
        return False

    lbl_src = src_labels / (stem + ".txt")

    # Copy image
    dst_images.mkdir(parents=True, exist_ok=True)
    shutil.copy2(img_src, dst_images / img_src.name)

    # Copy label (if it exists)
    if lbl_src.exists():
        dst_labels.mkdir(parents=True, exist_ok=True)
        shutil.copy2(lbl_src, dst_labels / lbl_src.name)
    else:
        print(f"  [INFO] No label for '{stem}' (background sample) — image only copied.")

    return True


def main():
    assert abs(TRAIN_RATIO + VAL_RATIO + TEST_RATIO - 1.0) < 1e-6, \
        "TRAIN_RATIO + VAL_RATIO + TEST_RATIO must equal 1.0"

    dataset  = Path(DATASET_DIR)
    src_imgs = dataset / "images"
    src_lbls = dataset / "labels"

    assert src_imgs.exists(), f"images/ folder not found at: {src_imgs}"
    assert src_lbls.exists(), f"labels/ folder not found at: {src_lbls}"

    # ── Collect all image stems ────────────────────────────────
    all_stems = [
        p.stem for p in src_imgs.iterdir()
        if p.suffix.lower() in IMAGE_EXTENSIONS
    ]

    if not all_stems:
        print("No images found. Check DATASET_DIR and IMAGE_EXTENSIONS.")
        return

    print(f"\nFound {len(all_stems)} images in {src_imgs}")

    # ── Group stems by primary class ───────────────────────────
    # class_index → [stem, stem, ...]
    class_groups: dict[int, list[str]]   = defaultdict(list)
    no_label_stems: list[str]            = []
    class_instance_counts: dict[int, int] = defaultdict(int)

    for stem in all_stems:
        lbl_path = src_lbls / (stem + ".txt")
        primary  = get_primary_class(lbl_path)

        if primary is None:
            no_label_stems.append(stem)
        else:
            class_groups[primary].append(stem)
            # Count total instances per class for the report
            with open(lbl_path, "r") as f:
                for line in f:
                    if line.strip():
                        cls = int(line.split()[0])
                        class_instance_counts[cls] += 1

    print(f"\nClass distribution (by primary class of each image):")
    print(f"  {'Class':<10} {'Images':>8}")
    print(f"  {'-'*20}")
    for cls in sorted(class_groups.keys()):
        print(f"  {cls:<10} {len(class_groups[cls]):>8}")
    if no_label_stems:
        print(f"  {'(no label)':<10} {len(no_label_stems):>8}")

    # ── Stratified split per class ─────────────────────────────
    train_stems, val_stems, test_stems = [], [], []

    for cls in sorted(class_groups.keys()):
        stems = class_groups[cls]
        tr, va, te = split_list(stems, TRAIN_RATIO, VAL_RATIO, RANDOM_SEED + cls)
        train_stems.extend(tr)
        val_stems.extend(va)
        test_stems.extend(te)

    # Background samples — random split
    if no_label_stems:
        tr, va, te = split_list(no_label_stems, TRAIN_RATIO, VAL_RATIO, RANDOM_SEED)
        train_stems.extend(tr)
        val_stems.extend(va)
        test_stems.extend(te)

    total = len(train_stems) + len(val_stems) + len(test_stems)
    print(f"\nSplit result:")
    print(f"  train : {len(train_stems):>4} images  ({len(train_stems)/total*100:.1f}%)")
    print(f"  val   : {len(val_stems):>4} images  ({len(val_stems)/total*100:.1f}%)")
    print(f"  test  : {len(test_stems):>4} images  ({len(test_stems)/total*100:.1f}%)")
    print(f"  total : {total:>4} images")

    # ── Create output folders and copy files ───────────────────
    splits = {
        "train": train_stems,
        "val":   val_stems,
        "test":  test_stems,
    }

    print("\nCopying files...")
    for split_name, stems in splits.items():
        dst_img = src_imgs / split_name
        dst_lbl = src_lbls / split_name
        copied  = 0

        for stem in stems:
            if copy_pair(stem, src_imgs, src_lbls,
                         dst_img, dst_lbl, IMAGE_EXTENSIONS):
                copied += 1

        print(f"  {split_name:<6}: {copied} files copied -> {dst_img}")

    # ── Write data.yaml ────────────────────────────────────────
    # Collect class names from all label files
    all_class_ids = sorted(
        set(int(line.split()[0])
            for lbl in src_lbls.glob("*.txt")
            if lbl.name != "classes.txt"
            for line in lbl.read_text().splitlines()
            if line.strip())
    )

    yaml_path = dataset / "data.yaml"
    with open(yaml_path, "w") as f:
        f.write(f"path: {dataset.as_posix()}\n")
        f.write(f"train: images/train\n")
        f.write(f"val:   images/val\n")
        f.write(f"test:  images/test\n")
        f.write(f"\nnc: {len(all_class_ids)}\n")
        f.write(f"# Replace the numbers below with your actual class names\n")
        f.write(f"names:\n")
        # Try to infer names from existing data.yaml if present
        existing_yaml = dataset / "data.yaml"
        # Write placeholder names — user should fill these in
        class_name_map = {
            0: "person",
            1: "animal",
            2: "vehicle",
            3: "personnel"
        }
        for cid in all_class_ids:
            name = class_name_map.get(cid, f"class_{cid}")
            f.write(f"  {cid}: {name}\n")

    print(f"\n data.yaml written to {yaml_path}")

    # ── Verification report ────────────────────────────────────
    print("\n── Verification ──────────────────────────────────────")
    for split_name in ["train", "val", "test"]:
        img_dir = src_imgs / split_name
        lbl_dir = src_lbls / split_name
        n_imgs  = len(list(img_dir.glob("*"))) if img_dir.exists() else 0
        n_lbls  = len(list(lbl_dir.glob("*.txt"))) if lbl_dir.exists() else 0
        print(f"  {split_name:<6}: {n_imgs} images, {n_lbls} labels")

    # ── Per-class instance counts ──────────────────────────────
    print("\n── Per-class instance counts across all splits ───────")
    print(f"  {'Class':<20} {'Train':>8} {'Val':>8} {'Test':>8} {'Total':>8}")
    print(f"  {'-'*48}")

    for split_name, stems in splits.items():
        pass  # computed below

    split_class_counts: dict[str, dict[int, int]] = {
        "train": defaultdict(int),
        "val":   defaultdict(int),
        "test":  defaultdict(int),
    }

    for split_name, stems in splits.items():
        lbl_dir = src_lbls / split_name
        for lbl_file in lbl_dir.glob("*.txt") if lbl_dir.exists() else []:
            for line in lbl_file.read_text().splitlines():
                if line.strip():
                    cls = int(line.split()[0])
                    split_class_counts[split_name][cls] += 1

    all_cls = sorted(
        set(c for d in split_class_counts.values() for c in d)
    )
    for cls in all_cls:
        tr = split_class_counts["train"].get(cls, 0)
        va = split_class_counts["val"].get(cls, 0)
        te = split_class_counts["test"].get(cls, 0)
        name = class_name_map.get(cls, f"class_{cls}")
        print(f"  {name:<20} {tr:>8} {va:>8} {te:>8} {tr+va+te:>8}")

    print("\n Dataset split complete.")
    print(f"\nNext step — train with:")
    print(f"  yolo detect train data={yaml_path} model=yolov8n.pt epochs=50 imgsz=640")


if __name__ == "__main__":
    main()