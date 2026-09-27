import os

# Folder containing YOLO labels
label_dir = r"C:\Users\User\Documents\my_miscellaneous_scripts\matched_annotations"

# Expansion factor for width
WIDTH_MULTIPLIER = 0.5

# Target class to modify
TARGET_CLASS = 1

for filename in os.listdir(label_dir):

    if not filename.endswith(".txt"):
        continue

    path = os.path.join(label_dir, filename)

    updated_lines = []

    with open(path, "r") as f:

        lines = f.readlines()

        for line in lines:

            parts = line.strip().split()

            # Skip invalid lines
            if len(parts) != 5:
                updated_lines.append(line.strip())
                continue

            cls_id = int(float(parts[0]))

            xc = float(parts[1])
            yc = float(parts[2])
            w  = float(parts[3])
            h  = float(parts[4])

            # Modify only target class
            if cls_id == TARGET_CLASS:

                # Expand width while keeping center fixed
                w = w * WIDTH_MULTIPLIER

                # Prevent overflow beyond image boundaries
                if xc - w / 2 < 0:
                    w = xc * 2

                if xc + w / 2 > 1:
                    w = (1 - xc) * 2

            updated_line = f"{cls_id} {xc} {yc} {w} {h}"
            updated_lines.append(updated_line)

    # Overwrite file
    with open(path, "w") as f:
        f.write("\n".join(updated_lines))

print("Width expansion complete.")