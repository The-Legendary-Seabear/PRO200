"""Exact-file and perceptual image hashing."""

import hashlib
import imagehash
from PIL import Image

def get_file_hash(file):
    sha256 = hashlib.sha256()
    with open(file, "rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def get_perceptual_hash(file):
    with Image.open(file) as image:
        return imagehash.phash(image)