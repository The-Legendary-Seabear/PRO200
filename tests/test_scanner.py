"""Tests for folder scanning."""

import tempfile
import unittest
from pathlib import Path

from photo_duplicate_finder.scanner import find_duplicates


class FindDuplicatesTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.folder = Path(self.temp_dir.name)
        self.subfolder = self.folder / "sub" / "deeper"
        self.subfolder.mkdir(parents=True)

        self.top_image = self.folder / "photo.jpg"
        self.nested_image = self.subfolder / "photo copy.jpg"
        self.top_image.write_bytes(b"same image data")
        self.nested_image.write_bytes(b"same image data")

    def test_top_level_only_ignores_subfolders(self):
        duplicates = find_duplicates(self.folder)

        self.assertEqual(duplicates, {})

    def test_include_subfolders_finds_nested_duplicates(self):
        duplicates = find_duplicates(self.folder, include_subfolders=True)

        self.assertEqual(len(duplicates), 1)
        files = next(iter(duplicates.values()))
        self.assertCountEqual(files, [self.top_image, self.nested_image])
