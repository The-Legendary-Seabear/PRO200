"""Folder traversal and exact/perceptual image discovery."""

from pathlib import Path

from photo_duplicate_finder.hashing import get_file_hash, get_perceptual_hash

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}


def get_image_files(folder_path, include_subfolders=False):
    """Return unique image paths from a folder, optionally recursively."""
    folder = Path(folder_path)
    if not folder.is_dir():
        raise NotADirectoryError(f"Folder does not exist: {folder}")

    entries = folder.rglob("*") if include_subfolders else folder.iterdir()
    # Resolving paths prevents a file in overlapping selected folders from
    # being compared against itself.
    return list(dict.fromkeys(
        path.resolve()
        for path in entries
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ))


def _hash_exact_files(files):
    """Group readable images by their SHA-256 hash."""
    hashes = {}
    for file_path in files:
        try:
            file_hash = get_file_hash(file_path)
        except OSError as error:
            print(f"Skipping unreadable file {file_path}: {error}")
            continue
        hashes.setdefault(file_hash, []).append(file_path)
    return hashes


def scan_folder(folder_path, include_subfolders=False):
    """Return all image paths grouped by SHA-256 hash."""
    return _hash_exact_files(get_image_files(folder_path, include_subfolders))


def find_duplicates(folder_path, include_subfolders=False):
    """Find byte-for-byte duplicate images inside a folder."""
    return {
        file_hash: files
        for file_hash, files in scan_folder(folder_path, include_subfolders).items()
        if len(files) > 1
    }


def _analyze_files(files, threshold=5):
    """Find exact groups and visually similar (but not exact) image pairs."""
    if threshold < 0:
        raise ValueError("Similarity threshold must be non-negative")

    hashes = _hash_exact_files(files)
    exact_hashes = {
        file_path: file_hash
        for file_hash, paths in hashes.items()
        for file_path in paths
    }
    duplicates = {
        file_hash: paths for file_hash, paths in hashes.items()
        if len(paths) > 1
    }

    perceptual_hashes = []
    for file_path in exact_hashes:
        try:
            perceptual_hashes.append((file_path, get_perceptual_hash(file_path)))
        except (OSError, ValueError) as error:
            print(f"Skipping invalid image {file_path}: {error}")

    similar_images = []
    for i in range(len(perceptual_hashes)):
        file1, hash1 = perceptual_hashes[i]
        for j in range(i + 1, len(perceptual_hashes)):
            file2, hash2 = perceptual_hashes[j]
            # Different files can have identical pHashes (distance 0), so
            # only exclude matches with identical *SHA-256* hashes.
            if exact_hashes[file1] == exact_hashes[file2]:
                continue
            difference = hash1 - hash2
            if difference <= threshold:
                similar_images.append((file1, file2, difference))

    return duplicates, similar_images


def find_similar_images(folder_path, threshold=5, include_subfolders=False):
    """Find visually similar, non-identical images inside a folder."""
    files = get_image_files(folder_path, include_subfolders)
    _, similar_images = _analyze_files(files, threshold)
    return similar_images


def compare_folders(folder_a, folder_b, include_subfolders=False, threshold=5):
    """Find matches within and across the combined contents of two folders."""
    all_files = list(dict.fromkeys(
        get_image_files(folder_a, include_subfolders)
        + get_image_files(folder_b, include_subfolders)
    ))
    return _analyze_files(all_files, threshold)
