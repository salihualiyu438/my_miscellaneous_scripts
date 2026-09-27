import os
import shutil

# ============================================================
# CONFIGURATION
# ============================================================

FOLDER_1 = r"C:\Users\User\Documents\my_miscellaneous_scripts\matched_images"
FOLDER_2 = r"C:\Users\User\Documents\final_year_project\datasets\masked_armed_bandit\combined_masked_armed_bandit__imagesllll"

OUTPUT_FOLDER = r"C:\Users\User\Documents\my_miscellaneous_scripts\unmatched_images"

FAILED_LOG = os.path.join(
    OUTPUT_FOLDER,
    "failed_files.txt"
)


# ============================================================
# IMAGE EXTENSIONS
# ============================================================

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
    ".tif",
    ".tiff"
}


# ============================================================
# CREATE OUTPUT FOLDER
# ============================================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ============================================================
# GET IMAGES FROM FOLDER 1
# ============================================================

folder_1_images = {
    filename.lower()
    for filename in os.listdir(FOLDER_1)
    if os.path.splitext(filename)[1].lower()
    in IMAGE_EXTENSIONS
}


# ============================================================
# GET IMAGES FROM FOLDER 2
# ============================================================

folder_2_images = [
    filename
    for filename in os.listdir(FOLDER_2)
    if os.path.splitext(filename)[1].lower()
    in IMAGE_EXTENSIONS
]


# ============================================================
# FIND IMAGES ONLY IN FOLDER 2
# ============================================================

images_only_in_folder_2 = [
    filename
    for filename in folder_2_images
    if filename.lower() not in folder_1_images
]


# ============================================================
# STATISTICS
# ============================================================

copied = 0
failed = 0


# ============================================================
# OPEN FAILURE LOG
# ============================================================

with open(
    FAILED_LOG,
    "w",
    encoding="utf-8"
) as log:

    # ========================================================
    # COPY FILES
    # ========================================================

    for count, filename in enumerate(
        images_only_in_folder_2,
        start=1
    ):

        source = os.path.join(
            FOLDER_2,
            filename
        )

        destination = os.path.join(
            OUTPUT_FOLDER,
            filename
        )

        try:

            shutil.copy2(
                source,
                destination
            )

            copied += 1

            print(
                f"[{count}/{len(images_only_in_folder_2)}] "
                f"Copied: {filename}"
            )

        except Exception as e:

            failed += 1

            print(
                f"\nERROR copying:\n"
                f"{filename}\n"
                f"Reason: {e}\n"
            )

            # Save details to log
            log.write(
                f"Filename: {filename}\n"
                f"Source: {source}\n"
                f"Destination: {destination}\n"
                f"Error: {repr(e)}\n"
                f"{'-' * 80}\n"
            )

            # IMPORTANT:
            # Continue with the next image
            continue


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("PROCESSING COMPLETE")
print("=" * 60)

print(f"Images in Folder 1          : {len(folder_1_images)}")
print(f"Images in Folder 2          : {len(folder_2_images)}")
print(
    f"Images only in Folder 2     : "
    f"{len(images_only_in_folder_2)}"
)

print(f"Successfully copied         : {copied}")
print(f"Failed to copy              : {failed}")

if failed > 0:

    print("\nSome files could not be copied.")

    print(
        f"See the failure log at:\n"
        f"{FAILED_LOG}"
    )

else:

    print("\nAll files were copied successfully.")

print("=" * 60)