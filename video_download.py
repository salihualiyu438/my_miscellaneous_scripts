# import requests

# url = "https://youtu.be/H4PGd_PBEns?t=22"
# output_file = "video.mp4"

# response = requests.get(url, stream=True)
# response.raise_for_status()

# with open(output_file, "wb") as file:
#     for chunk in response.iter_content(chunk_size=1024 * 1024):
#         if chunk:
#             file.write(chunk)

# print(f"Video downloaded successfully: {output_file}")

import yt_dlp

urls = ['https://youtube.com/shorts/Lu-OOwh4FC4?si=MAqEKynAAePcUwDi',
        'https://youtu.be/YcrZJmiJWuk?si=Fk0l0zQKPchTtI2i',
        'https://youtu.be/IM8De_YQP8o?si=qO88cVbjY_LvFW_X',
        'https://youtu.be/pv9fLVLSFvU?si=f6uJAfahh_H3_IxF',
        'https://youtube.com/shorts/97e1kD8AZQ0?si=98sA8AIgfid8ihqQ'
]

options = {
    "outtmpl": "%(title)s.%(ext)s",
    # "format": "bestvideo+bestaudio/best",
    "format": "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
}
for link in urls:

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([link])