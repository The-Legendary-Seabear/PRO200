"""Exact-file and perceptual image hashing."""

import hashlib

def get_file_hash(file):
    sha256 = hashlib.sha256()
    with open(file, "rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()