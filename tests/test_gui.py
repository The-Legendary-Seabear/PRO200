"""Tests for duplicate-group actions."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from photo_duplicate_finder.gui import keep_photo


class KeepPhotoTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.keeper = Path(self.temp_dir.name) / "keep.jpg"
        self.duplicate = Path(self.temp_dir.name) / "duplicate.jpg"
        self.keeper.touch()
        self.duplicate.touch()
        self.files = [self.keeper, self.duplicate]
        self.parent = Mock()
        self.refresh = Mock()
        self.next_group = Mock()

    @patch("photo_duplicate_finder.gui.messagebox.askyesno", return_value=True)
    def test_confirmed_keep_deletes_other_copies_and_advances(self, askyesno):
        keep_photo(
            self.parent,
            self.files,
            self.keeper,
            self.refresh,
            self.next_group,
        )

        self.assertTrue(self.keeper.exists())
        self.assertFalse(self.duplicate.exists())
        self.assertEqual(self.files, [self.keeper])
        self.next_group.assert_called_once_with()
        self.refresh.assert_not_called()
        askyesno.assert_called_once()

    @patch("photo_duplicate_finder.gui.messagebox.askyesno", return_value=False)
    def test_cancel_keeps_all_files_and_stays_on_group(self, askyesno):
        keep_photo(
            self.parent,
            self.files,
            self.keeper,
            self.refresh,
            self.next_group,
        )

        self.assertTrue(self.keeper.exists())
        self.assertTrue(self.duplicate.exists())
        self.assertEqual(self.files, [self.keeper, self.duplicate])
        self.next_group.assert_not_called()
        self.refresh.assert_not_called()
        askyesno.assert_called_once()

    def test_failed_delete_stays_on_group_and_reports_error(self):
        path_type = type(self.duplicate)
        original_unlink = path_type.unlink

        def unlink_with_failure(path, *args, **kwargs):
            if path == self.duplicate:
                raise PermissionError("file is locked")
            return original_unlink(path, *args, **kwargs)

        with (
            patch.object(path_type, "unlink", autospec=True, side_effect=unlink_with_failure),
            patch("photo_duplicate_finder.gui.messagebox.askyesno", return_value=True),
            patch("photo_duplicate_finder.gui.messagebox.showerror") as showerror,
        ):
            keep_photo(
                self.parent,
                self.files,
                self.keeper,
                self.refresh,
                self.next_group,
            )

        self.assertTrue(self.keeper.exists())
        self.assertTrue(self.duplicate.exists())
        self.assertEqual(self.files, [self.keeper, self.duplicate])
        self.next_group.assert_not_called()
        self.refresh.assert_called_once_with()
        showerror.assert_called_once()
