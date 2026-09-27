import os

# ── Change these two paths ───────────────────────────────────────────────────
SOURCE_FOLDER    = r"C:/Users/User/Documents/coen545 project/exam hall monitoring/dataset/labels/new_train"      # files to update
REFERENCE_FOLDER = r"C:/Users/User/Documents/coen545 project/exam hall monitoring/jonah2_annotation"  # new/updated files
# ────────────────────────────────────────────────────────────────────────────

source_folder    = os.path.abspath(SOURCE_FOLDER)
reference_folder = os.path.abspath(REFERENCE_FOLDER)

# Index all .txt files in the reference folder
reference_map = {}
for dirpath, _, filenames in os.walk(reference_folder):
    for filename in filenames:
        if filename.endswith(".txt"):
            reference_map[filename] = os.path.join(dirpath, filename)

print(f"Reference files found: {len(reference_map)}\n")

matched   = 0
unmatched = 0

# Traverse the source folder and overwrite matching files
for dirpath, _, filenames in os.walk(source_folder):
    for filename in filenames:
        if not filename.endswith(".txt"):
            continue

        source_path = os.path.join(dirpath, filename)

        if filename in reference_map:
            ref_path = reference_map[filename]

            # Read the reference file content
            with open(ref_path, "r", encoding="utf-8") as f:
                new_content = f.read()

            # Delete the source file
            os.remove(source_path)

            # Write the reference content as a fresh file
            with open(source_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            print(f"[UPDATED]  {source_path}")
            matched += 1
        else:
            print(f"[NO MATCH] {filename}")
            unmatched += 1

print(f"\nDone.  Updated: {matched}  |  No match: {unmatched}")