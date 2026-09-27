import os
import yt_dlp


# ==========================================================
# SETTINGS
# ==========================================================

PLAYLIST_URL = (
   "https://youtube.com/playlist?list=PL6xVgUZ4UP2Pn65Lt8WENDtmT9JDKoIft&si=um2FW1E_1WLXQP6O"
    # "https://youtube.com/playlist?"
    # "list=PLWnMeKaZKVEVRYk44I68r3gLjYYVTcybD"
)

DOWNLOAD_DIR = "Episodes"

ARCHIVE_FILE = "downloaded.txt"


# ==========================================================
# TITLE FILTER
# ==========================================================

def is_relevant_video(info, *, incomplete=False):

    title = info.get("title", "").lower()

    # Main series identifier
    if "the long ballad" not in title:
        return "Not a fateful love episode"

    return None


# ==========================================================
# FIND ENGLISH SUBTITLE
# ==========================================================

def find_english_subtitle(info):

    normal_subs = info.get("subtitles") or {}
    auto_subs = info.get("automatic_captions") or {}

    # ------------------------------------------------------
    # Prefer normal/manual English subtitles
    # ------------------------------------------------------

    for language in normal_subs:

        if language.lower().startswith("en"):
            return "normal", language

    # ------------------------------------------------------
    # Otherwise use automatic English captions
    # ------------------------------------------------------

    for language in auto_subs:

        if language.lower().startswith("en"):
            return "auto", language

    return None, None


# ==========================================================
# DOWNLOAD ONE EPISODE
# ==========================================================

def download_episode(url, index, title):

    print("\n" + "=" * 70)
    print(f"EPISODE {index}: {title}")
    print("=" * 70)

    # ------------------------------------------------------
    # Inspect video
    # ------------------------------------------------------

    inspect_options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(inspect_options) as ydl:

        info = ydl.extract_info(
            url,
            download=False
        )

    # ------------------------------------------------------
    # Find subtitle
    # ------------------------------------------------------

    subtitle_type, subtitle_language = (
        find_english_subtitle(info)
    )

    if subtitle_type == "normal":

        print(
            f"Subtitle selected: NORMAL English "
            f"({subtitle_language})"
        )

        use_normal_subtitles = True
        use_automatic_subtitles = False

    elif subtitle_type == "auto":

        print(
            f"Subtitle selected: AUTOMATIC English "
            f"({subtitle_language})"
        )

        use_normal_subtitles = False
        use_automatic_subtitles = True

    else:

        print("No English subtitle found.")

        use_normal_subtitles = False
        use_automatic_subtitles = False

    # ------------------------------------------------------
    # Output filename
    # ------------------------------------------------------

    output_template = (
        f"{DOWNLOAD_DIR}/"
        f"{index:03d} - %(title)s.%(ext)s"
    )

    # ------------------------------------------------------
    # yt-dlp options
    # ------------------------------------------------------

    options = {
        "cookiefile": "youtube_cookies.txt",

        "outtmpl": output_template,

        # ==================================================
        # VIDEO QUALITY
        # ==================================================
        "format": "bestvideo[height<=720]+bestaudio/best[height<=720]/best",

        # "format": (
        #     "bestvideo[height<=720]+bestaudio/"
        #     "best[height<=720]/best"
        # ),

        # ==================================================
        # SUBTITLES
        # ==================================================

        "writesubtitles": use_normal_subtitles,

        "writeautomaticsub": use_automatic_subtitles,

        "subtitleslangs": (
            [subtitle_language]
            if subtitle_language
            else []
        ),

        "subtitlesformat": "srt",

        # Embed subtitle inside MP4
        "embedsubs": (
            use_normal_subtitles
            or use_automatic_subtitles
        ),

        # ==================================================
        # OUTPUT
        # ==================================================

        "merge_output_format": "mp4",

        # ==================================================
        # DOWNLOAD RESUME / RETRIES
        # ==================================================

        "continuedl": True,

        "retries": 20,

        "fragment_retries": 20,

        "file_access_retries": 10,

        # ==================================================
        # ARCHIVE
        # ==================================================

        "download_archive": ARCHIVE_FILE,

        # ==================================================
        # ERROR HANDLING
        # ==================================================

        "ignoreerrors": True,

        # Don't overwrite completed files
        "nooverwrites": True,

        # ==================================================
        # PROGRESS
        # ==================================================

        "quiet": False,
    }

    with yt_dlp.YoutubeDL(options) as ydl:

        ydl.download([url])


# ==========================================================
# CREATE DOWNLOAD DIRECTORY
# ==========================================================

os.makedirs(
    DOWNLOAD_DIR,
    exist_ok=True
)


# ==========================================================
# GET PLAYLIST
# ==========================================================

playlist_options = {

    "quiet": True,

    "no_warnings": True,

    "extract_flat": True,

    "skip_download": True,
}


with yt_dlp.YoutubeDL(
    playlist_options
) as ydl:

    playlist = ydl.extract_info(
        PLAYLIST_URL,
        download=False
    )


entries = playlist.get(
    "entries",
    []
)


print("\n")
print("=" * 70)
print("PLAYLIST DOWNLOADER")
print("=" * 70)

print(
    f"Playlist entries found: {len(entries)}"
)

print(
    f"Download folder: {DOWNLOAD_DIR}"
)

print(
    f"Archive file: {ARCHIVE_FILE}"
)

print("=" * 70)


# ==========================================================
# PROCESS PLAYLIST
# ==========================================================

episode_number = 1


for entry in entries:

    if not entry:
        continue

    video_url = entry.get("url")

    title = entry.get(
        "title",
        "Unknown"
    )

    # ------------------------------------------------------
    # Check whether this is a relevant episode
    # ------------------------------------------------------

    if "the long ballad" not in title.lower():

        print(
            f"\nSKIPPING IRRELEVANT VIDEO:"
        )

        print(
            f"   {title}"
        )

        continue

    # ------------------------------------------------------
    # Download
    # ------------------------------------------------------

    try:

        download_episode(
            video_url,
            episode_number,
            title
        )

        episode_number += 1

    except Exception as error:

        print("\n" + "!" * 70)

        print(
            f"FAILED: {title}"
        )

        print(
            f"Reason: {error}"
        )

        print(
            "This episode will be retried "
            "when the script is run again."
        )

        print("!" * 70)

        continue


print("\n")
print("=" * 70)
print("PLAYLIST PROCESSING COMPLETED")
print("=" * 70)