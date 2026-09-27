# def files_checker(path_a, path_b):
#     import os

#     img_files = None
#     label_files = None

#     # paste the images path below
#     for dir_path, sub_dirs_names, files_names in os.walk(path_a):
#         img_files = files_names

#     # paste the labels path below
#     for dir_path, sub_dirs_names, files_names in os.walk(path_b):
#         label_files = files_names
#     is_smaller = min(len(img_files), len(label_files))


#     counter = 0
#     incrementor = 0
#     list_of_odds = list()
#     for i  in range(is_smaller):
#         if len(label_files) < len(img_files):
#             img_name, img_ext = os.path.splitext(img_files[i])
#             label_name, label_ext = os.path.splitext(label_files[incrementor])
#             if str(img_name) == str(label_name):
#                 print(img_name)
#                 counter+=1
#                 incrementor+=1
#             else:
#                 # incrementor-=1
#                 print(f'here is the odd file:  {img_name}')
#                 list_of_odds.append(f'{img_name} at index {i}')
#         else:
#             img_name, img_ext = os.path.splitext(img_files[incrementor])
#             label_name, label_ext = os.path.splitext(label_files[i])

#             if str(img_name) == str(label_name):
#                 print(img_name)
#                 counter+=1
#                 incrementor+=1
#             else:
#                 # incrementor-=1
#                 print(f'here is the odd file:  {img_name}')
#                 list_of_odds.append(f'{label_name} at index {i}')
        
#     print(counter)

#     print(list_of_odds)

# # calling the function
# files_checker("C:/Users/User/Documents/ready_footbal_fetched_frames", "C:/Users/User/Desktop/football_annotated_dset")

import shutil
from pathlib import Path

# ─────────────────────────────────────────────
#         PASTE YOUR FOLDER PATHS HERE
# ─────────────────────────────────────────────

# Folder that contains the misclassified annotation files (your reference)
SOURCE_DIR = Path(r"C:\Users\User\Documents\coen545 project\exam hall monitoring\annotated_datasets\rabiu\annotation")

# Your combined labels folder (files will be moved OUT of here)
COMBINED_DIR = Path(r"C:\Users\User\Documents\coen545 project\exam hall monitoring\dataset\combined\labels")

# Folder where the matched files will be moved to (will be created if it doesn't exist)
OUTPUT_DIR = Path(r"C:\Users\User\Documents\coen545 project\exam hall monitoring\dataset\combined\extracted_labels")

# ─────────────────────────────────────────────
#               SCRIPT STARTS HERE
# ─────────────────────────────────────────────

# Collect all file stems (names without extension) from the source folder
source_stems = {f.stem for f in SOURCE_DIR.iterdir() if f.is_file()}
print(f"Found {len(source_stems)} misclassified annotation(s) in source folder.")

# Collect all files from the combined labels folder, keyed by stem
combined_files = {f.stem: f for f in COMBINED_DIR.iterdir() if f.is_file()}
print(f"Found {len(combined_files)} annotation(s) in combined labels folder.")

# Create the output folder if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

moved = 0
missing = []

# Loop through each misclassified file and find its match in the combined folder
for stem in source_stems:
    if stem in combined_files:
        src_path = combined_files[stem]
        dst_path = OUTPUT_DIR / src_path.name

        shutil.move(str(src_path), str(dst_path))
        moved += 1
        print(f"  Moved: {src_path.name}")
    else:
        # File was in source but not found in combined folder
        missing.append(stem)
        print(f"  Not found in combined folder: '{stem}'")

# Summary
print(f"\nDone! Moved {moved} file(s) to '{OUTPUT_DIR}'")

# If any files were not found, save their names to a text file for review
if missing:
    missing_log = OUTPUT_DIR / "missing_files.txt"
    missing_log.write_text("\n".join(missing))
    print(f"{len(missing)} file(s) were not found. See: {missing_log}")