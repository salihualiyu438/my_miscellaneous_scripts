import os
import shutil
import cv2
import pathlib

sourcefolder = "C:/Users/User/Desktop/yolo_img_dataset_2/ready_footbal_fetched_frames_2"
destination_folder = "C:/Users/User/Desktop/yolo_img_dataset_2/ready_footbal_fetched_frames_3"
os.makedirs("C:/Users/User/Desktop/yolo_img_dataset_2/ready_footbal_fetched_frames_3", exist_ok=True)
count = 0
img_dir = pathlib.Path("C:/Users/User/Desktop/yolo_img_dataset_2/ready_footbal_fetched_frames_2")
for img in list(img_dir.glob("*/*.jpg")):
    image = str(img)
    cv2.imread(str(img))
    src_dir = os.path.join(sourcefolder, img)
    dst_dir = os.path.join(destination_folder, img)
    new_img_name = os.path.join(destination_folder, f"messi_frame{count}")
    cv2.imwrite(new_img_name ,img)
    print(f"{new_img_name} copied to {dst_dir}")
    count+=1
    print(f"{count} images copied to {dst_dir}")
