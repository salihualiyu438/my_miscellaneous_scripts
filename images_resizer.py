import os
from PIL import Image

# Input and output folders
input_folder = "C:/Users/User/Documents/final_year_project/datasets/selected_real_frames"
output_folder = "C:/Users/User/Documents/final_year_project/datasets/resized_selected_real_frames"
os.makedirs(output_folder, exist_ok=True)

# Target size for YOLOv8
target_size = (640, 640)

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # Preserve aspect ratio
        img.thumbnail(target_size, Image.Resampling.LANCZOS)

        # Create new image with black background
        new_img = Image.new("RGB", target_size, (0, 0, 0))
        offset_x = (target_size[0] - img.size[0]) // 2
        offset_y = (target_size[1] - img.size[1]) // 2
        new_img.paste(img, (offset_x, offset_y))

        # Save resized image
        new_img.save(os.path.join(output_folder, filename))

print("✅ All images resized to 640x640 with aspect ratio preserved!")
