import shutil
import os

frames_folder = r"C:\Users\User\Documents\final_year_project\extracted_real_frames\recording_20260831_165711"
# print(os.listdir(frames_folder))
counter = 1
divider = 15
dest = r"C:\Users\User\Documents\final_year_project\extracted_real_frames\recording_20260831_165711\selected"
os.makedirs(dest, exist_ok=True)

for file in os.listdir(frames_folder):
    file_dir = os.path.join(frames_folder, file)
    destination_dir = os.path.join(dest, file)

    if counter % divider == 0: # number 30 has been used
        shutil.copy(file_dir, destination_dir)
        print (f"{'='*80}")

        print(f'{os.path.basename(file)} copied from <==> {file_dir} to ==> {(destination_dir)}')
        print (f"{'='*80}")

    counter+=1
print(f'==> val: {int(counter/divider)} or ==> train: {int(counter/divider)*4} items have been copied')