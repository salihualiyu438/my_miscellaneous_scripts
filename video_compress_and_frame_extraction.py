"""
Video Compression + Frame Extractor for YOLO Dataset Preparation
================================================================
Compresses heavy phone-recorded videos and extracts frames suitable
for annotation and YOLO training.

Requirements:
    pip install opencv-python ffmpeg-python tqdm Pillow

Usage:
    python video_to_yolo_frames.py
    (edit CONFIG section below to match your setup)
"""

import cv2
import subprocess
import os
import sys
import hashlib
from pathlib import Path
from tqdm import tqdm
from PIL import Image


# ─────────────────────────────────────────────
#  CONFIG — Edit these to match your setup
# ─────────────────────────────────────────────

INPUT_DIR       = r"C:\Users\User\Documents\final_year_project\final year project online videos"         # Folder containing your phone videos
COMPRESSED_DIR  = r"C:\Users\User\Documents\final_year_project\20-08-2026_compressed_armed_videos"   # Where compressed videos will be saved
FRAMES_DIR      = r"C:\Users\User\Documents\final_year_project\20-08-2026-extracted_compressed_armed"              # Where extracted frames will be saved

# Compression settings
TARGET_WIDTH    = 640        # Resize to this width (height auto-scales, keep aspect ratio)
                              # Use 1920 for Full HD, 1280 for HD, 854 for 480p
VIDEO_CRF       = 28          # Quality: 18=near-lossless, 23=default, 28=good/smaller, 35=small/lower quality
VIDEO_FPS       = None        # Set to e.g. 15 to downsample FPS, or None to keep original

# Frame extraction settings
EXTRACT_FPS     = 2           # Extract this many frames per second (2 = 1 frame every 0.5s)
                              # Lower = fewer frames. Recommended: 1–3 for YOLO datasets
MIN_BLUR_SCORE  = 0         # Reject blurry frames below this Laplacian score (0 = keep all)
DEDUPLICATE     = True        # Skip frames that are too similar to the previous one
SIMILARITY_THRESH = 0.98      # How similar two frames must be to drop one (0–1, higher = stricter)

# Output frame settings
FRAME_FORMAT    = "jpg"       # "jpg" (smaller) or "png" (lossless)
FRAME_QUALITY   = 95          # JPEG quality (ignored for PNG)
MAX_FRAMES_PER_VIDEO = None   # Cap frames per video, or None for no limit

# Supported video extensions
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".3gp", ".hevc", ".m4v"}


# ─────────────────────────────────────────────
#  UTILITIES
# ─────────────────────────────────────────────

def check_ffmpeg():
    """Verify ffmpeg is installed."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def get_video_info(video_path: Path) -> dict:
    """Get duration, fps, resolution of a video using OpenCV."""
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return {}
    info = {
        "fps":      cap.get(cv2.CAP_PROP_FPS),
        "width":    int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height":   int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "frames":   int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        "duration": cap.get(cv2.CAP_PROP_FRAME_COUNT) / max(cap.get(cv2.CAP_PROP_FPS), 1),
    }
    cap.release()
    return info


def blur_score(frame) -> float:
    """Returns Laplacian variance — higher means sharper."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()


def frame_hash(frame) -> str:
    """Perceptual hash via small thumbnail for fast dedup."""
    small = cv2.resize(frame, (16, 16))
    gray  = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    return hashlib.md5(gray.tobytes()).hexdigest()


def frames_are_similar(f1, f2, threshold=0.97) -> bool:
    """Compare two frames using normalized histogram correlation."""
    h1 = cv2.calcHist([cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)], [0], None, [64], [0, 256])
    h2 = cv2.calcHist([cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)], [0], None, [64], [0, 256])
    cv2.normalize(h1, h1)
    cv2.normalize(h2, h2)
    score = cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL)
    return score >= threshold


# ─────────────────────────────────────────────
#  STEP 1: COMPRESS VIDEO
# ─────────────────────────────────────────────

def compress_video(input_path: Path, output_path: Path) -> bool:
    """
    Compress a video using ffmpeg with H.264, targeting a smaller resolution.
    Keeps aspect ratio. Skips if output already exists.
    """
    if output_path.exists():
        print(f"  [SKIP] Already compressed: {output_path.name}")
        return True

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Build scale filter — scale width to TARGET_WIDTH, auto height (divisible by 2)
    scale_filter = f"scale={TARGET_WIDTH}:-2"

    ffmpeg_cmd = [
        "ffmpeg", "-i", str(input_path),
        "-vcodec", "libx264",
        "-crf", str(VIDEO_CRF),
        "-preset", "fast",
        "-vf", scale_filter,
        "-acodec", "aac",
        "-movflags", "+faststart",  # Better for streaming/seeking
        "-y",                        # Overwrite without asking
    ]

    if VIDEO_FPS:
        ffmpeg_cmd += ["-r", str(VIDEO_FPS)]

    ffmpeg_cmd.append(str(output_path))

    print(f"  Compressing: {input_path.name} → {output_path.name}")
    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  [ERROR] ffmpeg failed:\n{result.stderr[-500:]}")
        return False

    # Print size comparison
    orig_mb  = input_path.stat().st_size  / 1e6
    new_mb   = output_path.stat().st_size / 1e6
    ratio    = (1 - new_mb / orig_mb) * 100
    print(f"  Size: {orig_mb:.1f} MB → {new_mb:.1f} MB  ({ratio:.0f}% reduction)")
    return True


# ─────────────────────────────────────────────
#  STEP 2: EXTRACT FRAMES
# ─────────────────────────────────────────────

def extract_frames(video_path: Path, output_folder: Path, start_count: int = 0) -> dict:
    """
    Extract frames from a video at EXTRACT_FPS, filtering blurry and duplicate frames.

    Frames are named after the OUTPUT FOLDER (not the video file), with a global
    counter starting at start_count — so numbering is continuous across all videos
    processed into the same folder.

    Example output: cats_000001.jpg, cats_000002.jpg, cats_000003.jpg …

    Returns stats dict including 'saved' so the caller can advance start_count.
    """
    output_folder.mkdir(parents=True, exist_ok=True)

    # Folder name is used as the frame name prefix
    folder_name = output_folder.name

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"  [ERROR] Cannot open: {video_path}")
        return {}

    video_fps    = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = max(1, int(round(video_fps / EXTRACT_FPS)))

    stats = {
        "total_read": 0, "saved": 0,
        "skipped_blur": 0, "skipped_dup": 0
    }

    prev_frame  = None
    frame_idx   = 0
    # Global counter — continues from wherever the previous video left off
    global_count = start_count

    with tqdm(total=total_frames, desc=f"  Extracting", unit="fr", leave=False) as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            pbar.update(1)
            stats["total_read"] += 1

            # Only process every Nth frame
            if frame_idx % frame_interval != 0:
                frame_idx += 1
                continue

            # Blur filter
            if MIN_BLUR_SCORE > 0:
                b = blur_score(frame)
                if b < MIN_BLUR_SCORE:
                    stats["skipped_blur"] += 1
                    frame_idx += 1
                    continue

            # Deduplication
            if DEDUPLICATE and prev_frame is not None:
                if frames_are_similar(frame, prev_frame, SIMILARITY_THRESH):
                    stats["skipped_dup"] += 1
                    frame_idx += 1
                    continue

            # Save frame — named after the folder with a 6-digit global number
            frame_name = f"{folder_name}_{global_count:06d}.{FRAME_FORMAT}"
            frame_path = output_folder / frame_name

            if FRAME_FORMAT == "jpg":
                cv2.imwrite(str(frame_path), frame,
                            [cv2.IMWRITE_JPEG_QUALITY, FRAME_QUALITY])
            else:
                cv2.imwrite(str(frame_path), frame)

            prev_frame    = frame
            global_count += 1
            stats["saved"] += 1

            if MAX_FRAMES_PER_VIDEO and stats["saved"] >= MAX_FRAMES_PER_VIDEO:
                print(f"  Reached frame cap ({MAX_FRAMES_PER_VIDEO}), stopping early.")
                break

            frame_idx += 1

    cap.release()
    return stats


# ─────────────────────────────────────────────
#  MAIN PIPELINE
# ─────────────────────────────────────────────

def main():
    print("\n" + "="*60)
    print("  VIDEO → YOLO FRAME EXTRACTOR")
    print("="*60)

    # Check ffmpeg
    if not check_ffmpeg():
        print("\n[ERROR] ffmpeg not found. Install it:")
        print("  Ubuntu/Debian : sudo apt install ffmpeg")
        print("  macOS         : brew install ffmpeg")
        print("  Windows       : https://ffmpeg.org/download.html")
        sys.exit(1)

    input_dir  = Path(INPUT_DIR)
    comp_dir   = Path(COMPRESSED_DIR)
    frames_dir = Path(FRAMES_DIR)

    if not input_dir.exists():
        print(f"\n[ERROR] Input folder not found: {input_dir.resolve()}")
        print("  Create it and place your videos inside.")
        sys.exit(1)

    # Find all videos
    videos = [f for f in input_dir.rglob("*") if f.suffix.lower() in VIDEO_EXTENSIONS]
    if not videos:
        print(f"\n[ERROR] No videos found in: {input_dir.resolve()}")
        sys.exit(1)

    print(f"\nFound {len(videos)} video(s) in '{input_dir}'\n")

    # All videos in one run share a single output folder named after INPUT_DIR.
    # e.g.  raw_videos/cats  →  frames/cats/cats_000001.jpg, cats_000002.jpg …
    shared_frame_dir   = frames_dir / input_dir.name
    global_frame_count = 0   # Continuous counter — no duplicate filenames across videos
    total_frames_saved = 0
    summary            = []

    print(f"Frames will be saved to: {shared_frame_dir.resolve()}\n")

    for i, video_path in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] {video_path.name}")

        info = get_video_info(video_path)
        if info:
            print(f"  Original: {info['width']}x{info['height']} @ {info['fps']:.1f}fps  |  "
                  f"{info['duration']:.1f}s  |  {video_path.stat().st_size/1e6:.1f} MB")

        # ── Step 1: Compress ──
        compressed_path = comp_dir / (video_path.stem + "_compressed.mp4")
        ok = compress_video(video_path, compressed_path)
        if not ok:
            print(f"  [SKIP] Skipping frame extraction due to compression error.")
            continue

        # ── Step 2: Extract frames ──
        # Pass global_frame_count so numbering continues from the last video
        print(f"  Extracting ~{EXTRACT_FPS} fps  |  numbering from {global_frame_count:06d}")
        stats = extract_frames(compressed_path, shared_frame_dir,
                               start_count=global_frame_count)

        if stats:
            print(f"  ✓ Saved {stats['saved']} frames  "
                  f"(blurry dropped: {stats['skipped_blur']}, "
                  f"duplicates dropped: {stats['skipped_dup']})")
            global_frame_count += stats["saved"]   # Advance so next video continues here
            total_frames_saved += stats["saved"]
            summary.append((video_path.name, stats["saved"]))

    # ── Summary ──
    print("\n" + "="*60)
    print(f"  DONE — {total_frames_saved} total frames extracted")
    print("="*60)
    for name, count in summary:
        print(f"  {name:<40} {count:>5} frames")
    print(f"\n  Frames saved to: {shared_frame_dir.resolve()}")
    print("  Next step: open the frames folder in your annotation tool.\n")


if __name__ == "__main__":
    main()
