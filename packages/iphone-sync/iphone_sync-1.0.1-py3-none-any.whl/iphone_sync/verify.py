from pathlib import Path

import cv2
from PIL import Image
from pillow_heif import open_heif  # type:ignore


def verify_video(file_path: Path):
    """Check if a .mov or .mp4 file is corrupted by trying to read frames."""
    cap = cv2.VideoCapture(str(file_path))
    if not cap.isOpened():
        return True  # File is likely corrupted
    ret, _ = cap.read()
    cap.release()
    return not ret  # If can't read a frame, it's corrupted


def verify_image(file_path: Path):
    """Check if an image file (.gif, .heic, .jpeg, .jpg, .png, .webp) is corrupted."""
    try:
        if file_path.suffix.lower() == ".heic":
            heif_file = open_heif(file_path)
            img = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,  # type:ignore
                "raw",
                heif_file.mode,
            )
            img.load()  # type:ignore
        else:
            img = Image.open(file_path)
            img.verify()  # Verify image integrity
        return False  # No corruption detected
    except Exception:
        return True  # Corrupt file


def verify_file(file_path: Path):
    ext = file_path.suffix.lower()
    if ext in {".mov", ".mp4"}:
        return verify_video(file_path)
    elif ext in {
        ".gif",
        ".heic",
        ".jpeg",
        ".jpg",
        ".png",
        ".webp",
    }:
        return verify_image(file_path)
    else:
        return False
