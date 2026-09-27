from ultralytics import YOLO

model = YOLO("nano.pt")      # or medium.pt

results = model.predict(
    source=r"C:\Users\User\Documents\final_year_project\datasets\last_combined_dataset\combined\image\person1_frames_1_1235.jpg",
    save=True,
    conf=0.25
)