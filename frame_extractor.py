import cv2
import os

# Path to your video file
video_path = r"C:\Users\User\Documents\my_miscellaneous_scripts\recordings\recording_20260831_165711.mp4"
video_name = os.path.basename(video_path)
video_name = video_name[:(len(video_name)-4)]
print (video_name)
# Output directory for frames
output_dir = f"C:/Users/User/Documents/final_year_project/extracted_real_frames/{video_name}"
os.makedirs(output_dir, exist_ok=True)

# Open the video
cap = cv2.VideoCapture(video_path)
frame_count = 0
counter = 0
while cap.isOpened():
    counter+=1
    ret, frame = cap.read()
    if not ret:
        print('no frame detected')
        break
    # Save frame as JPEG file
    frame_filename = os.path.join(output_dir, f'{video_name}_{frame_count:04d}.jpg')
    # frame_filename = os.path.join(output_dir, f'person_frames_8_{frame_count:04d}.jpg')
    print(f'frame name: {frame_filename}')
    if counter % 1 == 0:
        cv2.imwrite(frame_filename, frame)
        # print (f"{'='*80}")
        print(f"{os.path.basename(frame_filename)} succesfully extracted to {os.path.basename(output_dir)}")
        print (f"{'='*70}")
        frame_count += 1

cap.release()
print()
print (f"{'*'*100}")
print (f"{'*'*100}")
print()
print(f"Extracted {frame_count} frames to '{output_dir}'")
print()
print (f"{'_'*80}")
print (f"now there are a total of {len(os.listdir(output_dir))} files in {os.path.basename(output_dir)}")
print (f"{'_'*80}")