# -*- coding: utf-8 -*-
import shutil
import os

parent_folder = "C:/Users/User/Documents/coen545 project/exam hall monitoring/wolfson_videos_extracted_compressed"
root = os.path.split(parent_folder)[0]
head = os.path.split(parent_folder)[1]
save_dir = f"{root}/selected_{head}"
# print(os.listdir(frames_folder))
outer_counter = -1 # beacuse the root dir is also in consideration
inner_counter = 0
total = 0
divider = 20
os.makedirs(save_dir, exist_ok=True)
for dirpath, subdir, filenames in os.walk(parent_folder):
    for file in os.listdir(dirpath):
        file_dir = os.path.join(dirpath, file)
        destination_dir = os.path.join(save_dir, file)

        if (inner_counter % divider) == 0 and (os.path.isfile(file_dir)) and (os.path.exists(destination_dir) == False):

            shutil.copy(file_dir, destination_dir)
            print (f"{'='*80}")

            print(f'{os.path.basename(file)} copied from <==> {file_dir} to ==> {(destination_dir)}')
            print (f"{'='*80}")
        else:
            print("file already exists in the destination or file is not valid")

        inner_counter+=1
    total = inner_counter
    outer_counter+=1
    print(f"{'='*80}")
    print(f'{int(inner_counter/divider) } items have been copied')
    print(f"{'='*80}")
print()
print (f"total of {int(total/divider)} images have successfully been selected and copied from {outer_counter} subfolders")
print()
print(f"the files are saved in {save_dir}")
