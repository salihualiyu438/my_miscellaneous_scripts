from pathlib import Path

# ============================================================
# DATASET ROOT
# ============================================================

DATASET_ROOT = Path(
    r"C:\Users\User\Documents\final_year_project\datasets\august_combined_dataset\august_surveillance_dataset\august_surveillance_dataset"
)

# ============================================================
# FOLDERS TO PROCESS
# ============================================================

folders = [
    DATASET_ROOT / "images" / "train",
    DATASET_ROOT / "images" / "val",
    DATASET_ROOT / "labels" / "train",
    DATASET_ROOT / "labels" / "val",
]

# ============================================================
# RENAME FILES
# ============================================================

renamed_count = 0
skipped_count = 0

for folder in folders:

    if not folder.exists():
        print(f"\nWARNING: Folder does not exist:")
        print(folder)
        continue

    print(f"\nProcessing: {folder}")

    # Traverse all files recursively
    for file_path in folder.rglob("*"):

        if not file_path.is_file():
            continue

        # Only process filenames containing &
        if "&" not in file_path.name:
            continue

        # Replace & with and
        new_name = file_path.name.replace("&", "and")
        new_path = file_path.with_name(new_name)

        # Prevent accidental overwrite
        if new_path.exists():
            print(f"\nSKIPPED - Target already exists:")
            print(f"Old: {file_path.name}")
            print(f"New: {new_path.name}")

            skipped_count += 1
            continue

        try:
            file_path.rename(new_path)

            print(f"\nRenamed:")
            print(f"Old: {file_path.name}")
            print(f"New: {new_path.name}")

            renamed_count += 1

        except Exception as e:
            print(f"\nERROR renaming:")
            print(file_path)
            print(f"Error: {e}")


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("RENAMING COMPLETE")
print("=" * 60)

print(f"Files successfully renamed: {renamed_count}")
print(f"Files skipped: {skipped_count}")