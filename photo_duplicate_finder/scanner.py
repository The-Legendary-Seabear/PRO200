"""Folder traversal and image discovery."""
from pathlib import Path
from photo_duplicate_finder.hashing import get_file_hash

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}

def scan_folder(folder_path):
    hashes = {}

    folder = Path(folder_path)

    for file_path in folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
            file_hash = get_file_hash(file_path)

            if file_hash in hashes:
                hashes[file_hash].append(file_path)
            else:
                hashes[file_hash] = [file_path]

    return hashes

def find_duplicates(folder_path):
    hashes = scan_folder(folder_path)

    duplicates = {}

    for file_hash, files in hashes.items():
        if len(files) > 1:
            duplicates[file_hash] = files

    return duplicates