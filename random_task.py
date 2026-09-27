import os

# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FOLDER = r"C:\Users\User\Documents\my_miscellaneous_scripts\merged_annotations"

OUTPUT_FOLDER = r"C:\Users\User\Documents\my_miscellaneous_scripts\merged_annotations_modified"


# ============================================================
# REFERENCE BOUNDING BOX
# ============================================================

REFERENCE_WIDTH = 0.089844
REFERENCE_HEIGHT = 0.118056

# Calculate reference perimeter
REFERENCE_PERIMETER = 2 * (
    REFERENCE_WIDTH + REFERENCE_HEIGHT
)

print(f"Reference perimeter: {REFERENCE_PERIMETER:.6f}")


# ============================================================
# CLASS SETTINGS
# ============================================================

OLD_CLASS = 2
NEW_CLASS = 8


# ============================================================
# CREATE OUTPUT FOLDER
# ============================================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ============================================================
# STATISTICS
# ============================================================

total_files = 0
total_class_2 = 0
total_remapped = 0


# ============================================================
# PROCESS ANNOTATION FILES
# ============================================================

for filename in os.listdir(INPUT_FOLDER):

    if not filename.lower().endswith(".txt"):
        continue

    input_path = os.path.join(INPUT_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, filename)

    new_lines = []

    with open(input_path, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            parts = line.split()

            # YOLO annotation should contain:
            # class x_center y_center width height
            if len(parts) != 5:

                print(
                    f"WARNING: Invalid annotation "
                    f"in {filename}: {line}"
                )

                new_lines.append(line)
                continue

            try:
                class_id = int(parts[0])

                x_center = float(parts[1])
                y_center = float(parts[2])
                width = float(parts[3])
                height = float(parts[4])

            except ValueError:

                print(
                    f"WARNING: Could not read annotation "
                    f"in {filename}: {line}"
                )

                new_lines.append(line)
                continue


            # =================================================
            # CHECK CLASS 2
            # =================================================

            if class_id == OLD_CLASS:

                total_class_2 += 1

                # Calculate perimeter of this bounding box
                perimeter = 2 * (width + height)

                # Remap if perimeter is equal to or smaller
                # than the reference perimeter
                if perimeter <= REFERENCE_PERIMETER:

                    class_id = NEW_CLASS
                    total_remapped += 1

                    print(
                        f"Remapped {filename}: "
                        f"perimeter={perimeter:.6f} "
                        f"-> class {NEW_CLASS}"
                    )


            # =================================================
            # WRITE ANNOTATION LINE
            # =================================================

            new_line = (
                f"{class_id} "
                f"{x_center:.6f} "
                f"{y_center:.6f} "
                f"{width:.6f} "
                f"{height:.6f}"
            )

            new_lines.append(new_line)


    # ========================================================
    # SAVE NEW FILE
    # ========================================================

    with open(output_path, "w", encoding="utf-8") as f:

        for line in new_lines:
            f.write(line + "\n")

    total_files += 1


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("PROCESSING COMPLETE")
print("=" * 60)

print(f"Reference perimeter       : {REFERENCE_PERIMETER:.6f}")
print(f"Files processed            : {total_files}")
print(f"Class 2 labels found       : {total_class_2}")
print(f"Class 2 -> Class 8         : {total_remapped}")
print(f"Output folder              : {OUTPUT_FOLDER}")
print("=" * 60)

print("\nOriginal annotation folder was NOT modified.")