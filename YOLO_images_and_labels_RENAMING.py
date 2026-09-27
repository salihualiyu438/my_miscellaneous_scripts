import os
import shutil

# ============================================================
# CONFIGURATION
# ============================================================

IMAGE_FOLDER = r"C:\Users\User\Documents\final_year_project\datasets\august_dataset\august_gun_images"
ANNOTATION_FOLDER = r"C:\Users\User\Documents\final_year_project\datasets\august_dataset\august_gun_annotations"

OUTPUT_IMAGE_FOLDER = r"C:\Users\User\Documents\final_year_project\datasets\august_dataset\august_gun_images_renamed"
OUTPUT_ANNOTATION_FOLDER = r"C:\Users\User\Documents\final_year_project\datasets\august_dataset\august_gun_annotations_renamed"
# New filename format
PREFIX = "robof_gun_img"

# Starting number
START_NUMBER = 1


# ============================================================
# CREATE OUTPUT FOLDERS
# ============================================================

os.makedirs(OUTPUT_IMAGE_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_ANNOTATION_FOLDER, exist_ok=True)


# ============================================================
# GET IMAGES
# ============================================================

image_extensions = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
    ".tif",
    ".tiff"
}

images = [
    filename
    for filename in os.listdir(IMAGE_FOLDER)
    if os.path.splitext(filename)[1].lower() in image_extensions
]

# Sort so numbering is consistent
images.sort()


# ============================================================
# STATISTICS
# ============================================================

renamed_images = 0
renamed_annotations = 0
missing_annotations = 0


# ============================================================
# PROCESS EACH IMAGE
# ============================================================

for index, image_filename in enumerate(
    images,
    start=START_NUMBER
):

    # --------------------------------------------------------
    # Original image information
    # --------------------------------------------------------

    image_name, image_extension = os.path.splitext(
        image_filename
    )

    # Corresponding annotation
    annotation_filename = image_name + ".txt"

    annotation_path = os.path.join(
        ANNOTATION_FOLDER,
        annotation_filename
    )


    # --------------------------------------------------------
    # New filename
    # --------------------------------------------------------

    new_base_name = f"{PREFIX}_{index:03d}"

    new_image_filename = (
        new_base_name + image_extension
    )

    new_annotation_filename = (
        new_base_name + ".txt"
    )


    # --------------------------------------------------------
    # Copy image
    # --------------------------------------------------------

    source_image = os.path.join(
        IMAGE_FOLDER,
        image_filename
    )

    destination_image = os.path.join(
        OUTPUT_IMAGE_FOLDER,
        new_image_filename
    )

    shutil.copy2(
        source_image,
        destination_image
    )

    renamed_images += 1


    # --------------------------------------------------------
    # Copy corresponding annotation
    # --------------------------------------------------------

    if os.path.exists(annotation_path):

        destination_annotation = os.path.join(
            OUTPUT_ANNOTATION_FOLDER,
            new_annotation_filename
        )

        shutil.copy2(
            annotation_path,
            destination_annotation
        )

        renamed_annotations += 1

    else:

        missing_annotations += 1

        print(
            f"WARNING: No annotation found for "
            f"{image_filename}"
        )


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("RENAMING COMPLETE")
print("=" * 60)

print(f"Images processed        : {renamed_images}")
print(f"Annotations copied      : {renamed_annotations}")
print(f"Missing annotations     : {missing_annotations}")

print(f"\nRenamed images:")
print(OUTPUT_IMAGE_FOLDER)

print(f"\nRenamed annotations:")
print(OUTPUT_ANNOTATION_FOLDER)

print("\nOriginal folders were NOT modified.")
print("=" * 60)