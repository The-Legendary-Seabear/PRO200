"""Folder traversal and image discovery."""
from pathlib import Path
from photo_duplicate_finder.hashing import get_file_hash
from photo_duplicate_finder.hashing import get_perceptual_hash

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

def find_similar_images(folder_path, threshold=5):
    folder = Path(folder_path)
    image_hashes = []
    similar_images = []

    for file_path in folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
            perceptual_hash = get_perceptual_hash(file_path)
            image_hashes.append((file_path, perceptual_hash))

    for i in range(len(image_hashes)):
        for j in range(i + 1, len(image_hashes)):
            file1, hash1 = image_hashes[i]
            file2, hash2 = image_hashes[j]

            difference = hash1 - hash2

            if(difference == 0):
                continue
            if difference <= threshold:
                similar_images.append((file1, file2, difference))

    return similar_images