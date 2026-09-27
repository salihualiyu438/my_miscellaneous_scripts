import os
import shutil

# Folder containing annotation .txt files
label_folder = r"C:\Users\User\Documents\final_year_project\datasets\september_dataset\HUMAN DETECTOR\resized_labels"
new_files = f"{os.path.split(label_folder)[0]}/new_{os.path.basename(label_folder)}"
os.makedirs(new_files, exist_ok=True)

# Define class mapping (old_class: new_class)
class_mapping = {
    3:1,   # change class 7 → class 6
    4:2,
    5:3
    
    
}
counter=0
for filename in os.listdir(label_folder):
    if filename.endswith(".txt") & (filename != 'classes.txt'):
        file_path = os.path.join(label_folder, filename)
        dst_path = os.path.join(new_files, filename)
        shutil.copy(file_path, dst_path)

        with open(file_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()

            if len(parts) == 0:
                continue

            class_id = int(parts[0])

            # Replace class if in mapping
            if class_id in class_mapping:
                print("a class is found")
                class_id = class_mapping[class_id]

            parts[0] = str(class_id)
            new_lines.append(" ".join(parts))

        with open(file_path, "w") as f:
            f.write("\n".join(new_lines))
    counter+=1

print("Class remapping completed.")