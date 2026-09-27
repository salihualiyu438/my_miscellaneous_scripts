import cv2
from datetime import datetime
import os

# ==============================
# RTSP CAMERA SETTINGS
# ==============================
# RTSP_URL = "rtsp://admin:admin@192.168.0.172:554/12"
RTSP_URL = r"C:\Users\User\Downloads\IMG_0116.MOV"

# Folder where recordings will be saved
OUTPUT_DIR = "recordings"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
# CONNECT TO CAMERA
# ==============================
cap = cv2.VideoCapture(RTSP_URL)

if not cap.isOpened():
    print("ERROR: Could not connect to RTSP camera.")
    exit()

print("Connected to RTSP camera.")

# Get camera properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Some RTSP cameras don't report FPS correctly
if fps <= 0 or fps > 60:
    fps = 25

print(f"Resolution: {width}x{height}")
print(f"FPS: {fps}")

# ==============================
# CREATE RECORDING FILE
# ==============================
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

output_file = os.path.join(
    OUTPUT_DIR,
    f"recording_{timestamp}.mp4"
)

# MP4 codec
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

writer = cv2.VideoWriter(
    output_file,
    fourcc,
    fps,
    (width, height)
)

if not writer.isOpened():
    print("ERROR: Could not create video file.")
    cap.release()
    exit()

print(f"Recording started: {output_file}")
print("Press 'q' to stop recording.")

# ==============================
# RECORDING LOOP
# ==============================
while True:

    ret, frame = cap.read()

    if not ret:
        print("WARNING: Failed to read frame.")
        break

    # Display the live feed
    cv2.imshow("RTSP Camera", frame)

    # Save frame to video
    writer.write(frame)

    # Press q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ==============================
# CLEANUP
# ==============================
cap.release()
writer.release()
cv2.destroyAllWindows()

print(f"Recording saved to: {output_file}")