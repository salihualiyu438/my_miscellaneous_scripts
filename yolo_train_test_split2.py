import os
import shutil

# create a home path to save images and annotations
home1 = os.environ.get('HOMEPATH')
home2 = os.environ.get('HOME')

IMAGES_DIR = ""
LABELS_DIR = ""

# create directories to save the files
BASE_NAME1 = os.path.basename(IMAGES_DIR) # assuming both images and labels are in same directory
home = f"{home1 or home2}/{BASE_NAME}"


IMG_TRAIN_DEST = f"{home}/images/train"
IMG_VAL_DEST = f"{home}/images/val"
IMG_TEST_DEST = f"{home}/images/test"
LABELS_TRAIN_DEST = f"{home}/labels/train"
LABELS_VAL_DEST = f"{home}/labels/val"
LABELS_TEST_DEST = f"{home}/labels/test"
# dest_dirs = [IMG_TRAIN_DEST, IMG_VAL_DEST, IMG_TEST_DEST, LABELS_TRAIN_DEST, LABELS_VAL_DEST, LABELS_TEST_DEST]
# dirs = (i for i in dest_dirs)
os.makedirs(IMG_TRAIN_DEST, exist_ok=True)
os.makedirs(IMG_VAL_DEST, exist_ok=True)
os.makedirs(IMG_TEST_DEST, exist_ok=True)
os.makedirs(LABELS_TRAIN_DEST, exist_ok=True)
os.makedirs(LABELS_VAL_DEST, exist_ok=True)
os.makedirs(LABELS_TEST_DEST, exist_ok=True)
# define valid extensions for images
valid_ext = ['jpg', 'jpeg', 'png', 'webp']


# for file in os.listdir(IMAGES_DIR):
#     img_path = os.path.join(IMAGES_DIR, file)
#     root_name = os.path.splitext(file_path)[0]
#     label_path = os.path.join(LABELS_DIR, root_name + '.txt')
#     if os.path.splitext(img_path)[1].lower() in valid_ext and os.path.exists(label_path):
