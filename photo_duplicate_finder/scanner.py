"""Folder traversal and image discovery."""
from photo_duplicate_finder.hashing import get_file_hash

def scanFolder(folder_path):
    hashes = {}