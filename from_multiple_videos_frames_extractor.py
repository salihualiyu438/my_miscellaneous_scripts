import cv2
import os

# Path to your video file
parent_folder = r"C:\Users\User\Documents\my_miscellaneous_scripts\infra_record"
# Output directory for frames
root = os.path.split(parent_folder)[1]
output_dir = f"C:/Users/User/Documents/final_year_project/datasets/september_dataset/HUMAN_DETECTOR/{root}_extracted_uncompressed"
os.makedirs(output_dir, exist_ok=True)
supported_extensions = ['.mp4', '.mov', '.MOV', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.mpeg', '.mpg', '.3gp', '.ogv']

outer_loop_count = 0
folder_count = 0
vid_count = None
class_name = os.path.split(parent_folder)[1]
# frame_filename = None
for dirpath, subdirs, files in os.walk(parent_folder):
    if len(files) >= 1:
        folder_count +=1
        vid_count = 0
        for file in os.listdir(dirpath):
            file_dir = os.path.join(dirpath, file)
            print(file_dir)
            if os.path.isfile(file_dir) and  os.path.splitext(file_dir)[1] in supported_extensions:
                # Open the video
                cap = cv2.VideoCapture(file_dir)
                frame_count = 0
                counter = 0
                while cap.isOpened():
                    counter+=1
                    ret, frame = cap.read()
                    if not ret:
                        break
                    # Save frame as JPEG file
                    frame_filename = os.path.join(output_dir, f'{class_name}{folder_count}_frames_{vid_count}_{frame_count:04d}.jpg')
                    if os.path.exists(frame_filename):
                        continue
                    if counter % 15 == 0:
                        cv2.imwrite(frame_filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                        # print (f"{'='*80}")
                        print(f"{os.path.split(frame_filename)[1]} succesfully extracted to {os.path.basename(output_dir)}")
                        print (f"{'='*70}")
                        frame_count += 1

                cap.release()
                print()
                print (f"{'*'*100}")
                print (f"{'*'*100}")
                print()
                print(f"Extracted {frame_count} frames from {os.path.basename(dirpath)} to '{os.path.basename(output_dir)}'")
                print()
            else:
                print("no video file found in", os.path.basename(dirpath))
                print(os.path.splitext(file))
            vid_count += 1
    outer_loop_count += 1
    print(f"total number of videos found here: {vid_count}")
print (f"total number of folders found with videos: {folder_count}")

print (f"{'_'*80}")
print (f"now there are a total of {len(os.listdir(output_dir))} files in {os.path.basename(output_dir)}")
print (f"{'_'*80}")
print(outer_loop_count)