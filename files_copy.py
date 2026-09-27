import os
import shutil

FILES_PATH = "C:/Users/User/Documents/NLP_project/cv-corpus-25.0-2026-03-09/ha/wav_clips"
DEST_PATH = "F:/wav_clips"
count=0
for file in os.listdir(FILES_PATH):
    src = os.path.join(FILES_PATH, file)
    dst = os.path.join(DEST_PATH, file)
    shutil.copy2(src, dst)
    if count%20 == 1:
        print (f"copied {count} files")
    count+=1
print (f"successfully copied {count} files")