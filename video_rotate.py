import cv2

input_video = r"C:\Users\User\Documents\final_year_project\final year project custom video dataset\security_personnels\august videos\IMG_0045.MOV"
output_video = "rotated_video.mp4"

# Open the video
cap = cv2.VideoCapture(input_video)

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Rotation option
# rotation = cv2.ROTATE_90_CLOCKWISE
# Other options:
rotation = cv2.ROTATE_90_COUNTERCLOCKWISE
# cv2.ROTATE_180

# For 90° or 270°, width and height are swapped
if rotation in [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_90_COUNTERCLOCKWISE]:
    output_size = (height, width)
else:
    output_size = (width, height)

# Create output video
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_video, fourcc, fps, output_size)

# Process each frame
while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Rotate frame
    rotated_frame = cv2.rotate(frame, rotation)

    # Save rotated frame
    out.write(rotated_frame)

# Release resources
cap.release()
out.release()

print("Video rotated successfully!")