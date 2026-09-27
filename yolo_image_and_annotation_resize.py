import os
from PIL import Image

# ============================================================
# CONFIGURATION
# ============================================================

images_folder = r"C:\Users\User\Documents\final_year_project\datasets\september_dataset\HUMAN DETECTOR\infra_record_extract\matched_images"
labels_folder = r"C:\Users\User\Documents\final_year_project\datasets\september_dataset\HUMAN DETECTOR\infra_record_extract\matched_annotations"

output_images_folder = r"C:\Users\User\Documents\final_year_project\datasets\september_dataset\HUMAN DETECTOR\infra_record_extract\resized_images"
output_labels_folder = r"C:\Users\User\Documents\final_year_project\datasets\september_dataset\HUMAN DETECTOR\infra_record_extract\resized_labels"

TARGET_WIDTH = 640
TARGET_HEIGHT = 640

image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


# ============================================================
# CREATE OUTPUT FOLDERS
# ============================================================

os.makedirs(output_images_folder, exist_ok=True)
os.makedirs(output_labels_folder, exist_ok=True)


# ============================================================
# PROCESS IMAGES
# ============================================================

for filename in os.listdir(images_folder):

    if not filename.lower().endswith(image_extensions):
        continue

    image_path = os.path.join(images_folder, filename)

    image_name = os.path.splitext(filename)[0]
    label_filename = image_name + ".txt"
    label_path = os.path.join(labels_folder, label_filename)

    output_image_path = os.path.join(
        output_images_folder,
        filename
    )

    output_label_path = os.path.join(
        output_labels_folder,
        label_filename
    )

    try:

        # ----------------------------------------------------
        # OPEN IMAGE
        # ----------------------------------------------------

        image = Image.open(image_path).convert("RGB")

        original_width, original_height = image.size

        # ----------------------------------------------------
        # CALCULATE SCALE
        # ----------------------------------------------------

        scale = min(
            TARGET_WIDTH / original_width,
            TARGET_HEIGHT / original_height
        )

        new_width = round(original_width * scale)
        new_height = round(original_height * scale)

        # ----------------------------------------------------
        # RESIZE IMAGE WHILE KEEPING ASPECT RATIO
        # ----------------------------------------------------

        resized = image.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )

        # ----------------------------------------------------
        # CREATE 640x640 CANVAS
        # ----------------------------------------------------

        canvas = Image.new(
            "RGB",
            (TARGET_WIDTH, TARGET_HEIGHT),
            (114, 114, 114)
        )

        # Calculate padding
        pad_x = (TARGET_WIDTH - new_width) / 2
        pad_y = (TARGET_HEIGHT - new_height) / 2

        pad_x_int = round(pad_x)
        pad_y_int = round(pad_y)

        # Paste resized image onto canvas
        canvas.paste(
            resized,
            (pad_x_int, pad_y_int)
        )

        # ----------------------------------------------------
        # SAVE RESIZED IMAGE
        # ----------------------------------------------------

        canvas.save(output_image_path)

        # ----------------------------------------------------
        # PROCESS YOLO ANNOTATIONS
        # ----------------------------------------------------

        if os.path.exists(label_path):

            with open(label_path, "r") as f:
                lines = f.readlines()

            new_annotations = []

            for line in lines:

                line = line.strip()

                if not line:
                    continue

                parts = line.split()

                if len(parts) != 5:
                    print(
                        f"Invalid annotation format: {label_path}"
                    )
                    continue

                class_id = parts[0]

                # Original YOLO normalized coordinates
                x_center = float(parts[1])
                y_center = float(parts[2])
                box_width = float(parts[3])
                box_height = float(parts[4])

                # ------------------------------------------------
                # CONVERT NORMALIZED COORDINATES TO PIXELS
                # ------------------------------------------------

                x_center_pixel = x_center * original_width
                y_center_pixel = y_center * original_height

                box_width_pixel = box_width * original_width
                box_height_pixel = box_height * original_height

                # ------------------------------------------------
                # SCALE BOUNDING BOX
                # ------------------------------------------------

                x_center_pixel = (
                    x_center_pixel * scale
                ) + pad_x

                y_center_pixel = (
                    y_center_pixel * scale
                ) + pad_y

                box_width_pixel *= scale
                box_height_pixel *= scale

                # ------------------------------------------------
                # CONVERT BACK TO YOLO NORMALIZED FORMAT
                # ------------------------------------------------

                new_x_center = (
                    x_center_pixel / TARGET_WIDTH
                )

                new_y_center = (
                    y_center_pixel / TARGET_HEIGHT
                )

                new_box_width = (
                    box_width_pixel / TARGET_WIDTH
                )

                new_box_height = (
                    box_height_pixel / TARGET_HEIGHT
                )

                # ------------------------------------------------
                # SAVE NEW ANNOTATION
                # ------------------------------------------------

                new_annotations.append(
                    f"{class_id} "
                    f"{new_x_center:.6f} "
                    f"{new_y_center:.6f} "
                    f"{new_box_width:.6f} "
                    f"{new_box_height:.6f}\n"
                )

            # ----------------------------------------------------
            # SAVE ANNOTATION
            # ----------------------------------------------------

            with open(output_label_path, "w") as f:
                f.writelines(new_annotations)

        else:

            print(
                f"No annotation found for: {filename}"
            )

        print(f"Processed: {filename}")

    except Exception as e:

        print(
            f"ERROR processing {filename}: {e}"
        )


# ============================================================
# FINISHED
# ============================================================

print("\n========================================")
print("DONE")
print("========================================")
print(f"Images saved to: {output_images_folder}")
print(f"Labels saved to: {output_labels_folder}")