import shutil
import os

frames_folder = "C:/Users/User/Documents/final_year_project/extracted_compressed_images_folder/vehicles_extracted_compressed"

# print(os.listdir(frames_folder))
counter = 1
divider = int(len(os.listdir(frames_folder))/1000)
os.makedirs("C:/Users/User/Documents/final_year_project/extracted_compressed_images_folder/selected_vehicles_extracted_compressed", exist_ok=True)
for file in os.listdir(frames_folder):
    file_dir = os.path.join(frames_folder, file)
    destination_dir = os.path.join("C:/Users/User/Documents/final_year_project/extracted_compressed_images_folder/selected_vehicles_extracted_compressed", file)

    if counter % divider == 0: # number 30 has been used
        shutil.copy(file_dir, destination_dir)
        print (f"{'='*80}")

        print(f'{os.path.basename(file)} copied from <==> {file_dir} to ==> {(destination_dir)}')
        print (f"{'='*80}")

    counter+=1
print(f'==> val: {int(counter/divider)} or ==> train: {int(counter/divider)*4} items have been copied')