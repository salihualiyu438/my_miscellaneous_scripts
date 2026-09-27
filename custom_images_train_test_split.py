import os
import shutil

# مسیر to your dataset (CHANGE THIS)
SOURCE_DIR = "C:/Users/User/Documents/deep_learning_project/dataset"
DEST_DIR = "labeled_dataset"

# Emotion mapping
emotion_map = {
    "ne": "neutral",
    "ex": "excited",
    "sa": "sad",
    "an": "angry",
    "ha": "happy",
    "fr": "frustrated",
    "su": "surprised",
    "di": "disgust",
    "fe": "fear"
}

def extract_emotion(filename):
    """
    Extract emotion code from filename.
    Example: Ses01M_impro03_F017_ne0.png -> ne
    """
    name = os.path.splitext(filename)[0]
    parts = name.split("_")
    
    if len(parts) < 4:
        return None
    
    last_part = parts[-1]  # e.g., ne0
    emotion_code = last_part[:2]  # first 2 chars
    
    return emotion_code


def main():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    for file in os.listdir(SOURCE_DIR):
        if not file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        emotion_code = extract_emotion(file)

        if emotion_code not in emotion_map:
            print(f"Skipping unknown label: {file}")
            continue

        emotion_name = emotion_map[emotion_code]

        # Create class folder
        class_dir = os.path.join(DEST_DIR, emotion_name)
        os.makedirs(class_dir, exist_ok=True)

        # Copy file
        src_path = os.path.join(SOURCE_DIR, file)
        dst_path = os.path.join(class_dir, file)

        shutil.copy(src_path, dst_path)

    print(" Dataset labeling complete!")


if __name__ == "__main__":
    main()