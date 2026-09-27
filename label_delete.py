import os

# ============================================================
# SETTINGS
# ============================================================

# Folder containing your original YOLO annotation files
INPUT_FOLDER = r"C:\Users\User\Documents\final_year_project\extracted_compressed_images_folder\annot_selected_youtube_extracted_uncompressed"

# New folder where modified annotations will be saved
OUTPUT_FOLDER = r"C:\Users\User\Documents\final_year_project\extracted_compressed_images_folder\new_annot_selected_youtube_extracted_uncompressed"

# Class IDs you want to DELETE
CLASSES_TO_DELETE = {0, 1, 3, 4, 5, 6, 7}


# ============================================================
# CREATE OUTPUT FOLDER
# ============================================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ============================================================
# PROCESS ANNOTATION FILES
# ============================================================

total_files = 0
modified_files = 0
deleted_annotations = 0

for filename in os.listdir(INPUT_FOLDER):

    # Only process .txt files
    if not filename.lower().endswith(".txt"):
        continue

    total_files += 1

    input_path = os.path.join(INPUT_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, filename)

    kept_lines = []
    file_deleted = 0

    # Read annotation file
    with open(input_path, "r") as file:
        lines = file.readlines()

    # Check every annotation
    for line in lines:

        line = line.strip()

        # Ignore empty lines
        if not line:
            continue

        parts = line.split()

        # First value is the YOLO class ID
        class_id = int(parts[0])

        # Delete annotation if class is in CLASSES_TO_DELETE
        if class_id in CLASSES_TO_DELETE:
            file_deleted += 1
            deleted_annotations += 1
        else:
            kept_lines.append(line)

    # Save result in the NEW folder
    with open(output_path, "w") as file:
        for line in kept_lines:
            file.write(line + "\n")

    if file_deleted > 0:
        modified_files += 1


# ============================================================
# SUMMARY
# ============================================================

print("=" * 50)
print("ANNOTATION PROCESSING COMPLETED")
print("=" * 50)

print(f"Total annotation files: {total_files}")
print(f"Files modified:         {modified_files}")
print(f"Annotations deleted:    {deleted_annotations}")
print(f"Output folder:          {OUTPUT_FOLDER}")

print("=" * 50)