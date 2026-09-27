import os

# Change this to your dataset folder
dataset_folder = r"C:\Users\User\Documents\final_year_project\datasets\september_dataset\WEAPON DETECTOR\resized_dataset"

folders = [
    os.path.join(dataset_folder, "images", "train"),
    os.path.join(dataset_folder, "images", "val"),
    os.path.join(dataset_folder, "images", "test"),

    os.path.join(dataset_folder, "labels", "train"),
    os.path.join(dataset_folder, "labels", "val"),
    os.path.join(dataset_folder, "labels", "test"),
]

renamed_count = 0

for folder in folders:

    if not os.path.exists(folder):
        print(f"Folder not found: {folder}")
        continue

    for filename in os.listdir(folder):

        if "&" not in filename:
            continue

        old_path = os.path.join(folder, filename)

        # Replace & with and
        new_filename = filename.replace("&", "and")
        new_path = os.path.join(folder, new_filename)

        # Prevent accidental overwrite
        if os.path.exists(new_path):
            print(f"SKIPPED (target already exists): {filename}")
            continue

        os.rename(old_path, new_path)

        print(f"Renamed: {filename}  ->  {new_filename}")
        renamed_count += 1


print("\n================================")
print("DONE")
print("================================")
print(f"Files renamed: {renamed_count}")