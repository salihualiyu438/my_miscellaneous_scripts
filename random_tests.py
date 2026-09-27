import os

print(os.getcwd())
print(os.listdir(os.getcwd()))
parent_folder = "C:/Users/User/Documents/final_year_project/datasets/real_frames"

for dir_path, sub_dirs_names, files_names in (os.walk(parent_folder)): # this returns 3 things:- dir_path, sub_dirs_names, files_names
    # for file in dir_path:
    print('parent_directory:', dir_path)
    print(f'sub_dirs_in{dir_path}:', sub_dirs_names)
    print(f'files in {dir_path}:', files_names[:2])
    # print(" files names:  hidden")