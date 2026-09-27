import os

# ============================================================
# CONFIGURATION
# ============================================================

FOLDER_1 = r"C:\Users\User\Documents\final_year_project\datasets\done\selected_extracted_compressed_images_folder\annot_selected_person_extracted_compressed"
FOLDER_2 = r"C:\Users\User\Documents\final_year_project\datasets\head_detect_annot_persons_images"
OUTPUT_FOLDER = r"C:\Users\User\Documents\final_year_project\datasets\august_persons_annotations"


# ============================================================
# CREATE OUTPUT FOLDER
# ============================================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ============================================================
# GET ALL TXT FILES
# ============================================================

files_1 = {
    filename
    for filename in os.listdir(FOLDER_1)
    if filename.lower().endswith(".txt")
}

files_2 = {
    filename
    for filename in os.listdir(FOLDER_2)
    if filename.lower().endswith(".txt")
}


# Get all unique annotation filenames
all_files = sorted(files_1 | files_2)


print(f"Folder 1 annotation files: {len(files_1)}")
print(f"Folder 2 annotation files: {len(files_2)}")
print(f"Total unique files:        {len(all_files)}")


# ============================================================
# MERGE FILES
# ============================================================

for filename in all_files:

    annotations = []

    # --------------------------------------------------------
    # READ FOLDER 1
    # --------------------------------------------------------

    if filename in files_1:

        file_path_1 = os.path.join(
            FOLDER_1,
            filename
        )

        with open(file_path_1, "r", encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                if line:
                    annotations.append(line)


    # --------------------------------------------------------
    # READ FOLDER 2
    # --------------------------------------------------------

    if filename in files_2:

        file_path_2 = os.path.join(
            FOLDER_2,
            filename
        )

        with open(file_path_2, "r", encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                if line:
                    annotations.append(line)


    # --------------------------------------------------------
    # REMOVE EXACT DUPLICATES
    # --------------------------------------------------------

    annotations = list(dict.fromkeys(annotations))


    # --------------------------------------------------------
    # WRITE MERGED FILE
    # --------------------------------------------------------

    output_path = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    with open(output_path, "w", encoding="utf-8") as f:

        for annotation in annotations:
            f.write(annotation + "\n")


# ============================================================
# FINISHED
# ============================================================

print("\nMerge completed successfully.")
print(f"Merged annotations saved to:\n{OUTPUT_FOLDER}")