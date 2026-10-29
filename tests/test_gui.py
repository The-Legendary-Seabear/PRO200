"""Tests for duplicate-group actions."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from photo_duplicate_finder.gui import delete_selected, keep_selected


class DeleteSelectedTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.keeper = Path(self.temp_dir.name) / "keep.jpg"
        self.duplicate = Path(self.temp_dir.name) / "duplicate.jpg"
        self.second_keeper = Path(self.temp_dir.name) / "second-keep.jpg"
        self.keeper.touch()
        self.duplicate.touch()
        self.second_keeper.touch()
        self.files = [self.keeper, self.duplicate]
        self.parent = Mock()
        self.refresh = Mock()
        self.next_group = Mock()

    @patch("photo_duplicate_finder.gui.messagebox.askyesno", return_value=True)
    def test_confirmed_delete_removes_only_marked_images(
        self, askyesno
    ):
        self.files.append(self.second_keeper)
        delete_selected(
            self.parent,
            self.files,
            {self.duplicate},
            self.refresh,
            self.next_group,
        )

        self.assertTrue(self.keeper.exists())
        self.assertFalse(self.duplicate.exists())
        self.assertTrue(self.second_keeper.exists())
        self.assertEqual(self.files, [self.keeper, self.second_keeper])
        self.next_group.assert_called_once_with()
        self.refresh.assert_not_called()
        askyesno.assert_called_once()

    @patch("photo_duplicate_finder.gui.messagebox.askyesno", return_value=False)
    def test_cancel_keeps_all_files_and_stays_on_group(self, askyesno):
        delete_selected(
            self.parent,
            self.files,
            {self.duplicate},
            self.refresh,
            self.next_group,
        )

        self.assertTrue(self.keeper.exists())
        self.assertTrue(self.duplicate.exists())
        self.assertEqual(self.files, [self.keeper, self.duplicate])
        self.next_group.assert_not_called()
        self.refresh.assert_not_called()
        askyesno.assert_called_once()

    @patch("photo_duplicate_finder.gui.messagebox.showinfo")
    def test_no_marked_files_does_not_prompt_or_advance(self, showinfo):
        with patch("photo_duplicate_finder.gui.messagebox.askyesno") as askyesno:
            delete_selected(
                self.parent,
                self.files,
                set(),
                self.refresh,
                self.next_group,
            )

        self.assertTrue(self.keeper.exists())
        self.assertTrue(self.duplicate.exists())
        self.next_group.assert_not_called()
        askyesno.assert_not_called()
        showinfo.assert_called_once()

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
            delete_selected(
                self.parent,
                self.files,
                {self.duplicate},
                self.refresh,
                self.next_group,
            )

        self.assertTrue(self.keeper.exists())
        self.assertTrue(self.duplicate.exists())
        self.assertEqual(self.files, [self.keeper, self.duplicate])
        self.next_group.assert_not_called()
        self.refresh.assert_called_once_with()
        showerror.assert_called_once()


class KeepSelectedTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.first = Path(self.temp_dir.name) / "first.jpg"
        self.second = Path(self.temp_dir.name) / "second.jpg"
        self.third = Path(self.temp_dir.name) / "third.jpg"
        for path in (self.first, self.second, self.third):
            path.touch()
        self.files = [self.first, self.second, self.third]
        self.parent = Mock()
        self.refresh = Mock()
        self.next_group = Mock()

    @patch("photo_duplicate_finder.gui.messagebox.askyesno", return_value=True)
    def test_confirmed_keep_selected_deletes_only_unselected(self, askyesno):
        keep_selected(
            self.parent,
            self.files,
            {self.first, self.third},
            self.refresh,
            self.next_group,
        )

        self.assertTrue(self.first.exists())
        self.assertFalse(self.second.exists())
        self.assertTrue(self.third.exists())
        self.assertEqual(self.files, [self.first, self.third])
        self.next_group.assert_called_once_with()
        askyesno.assert_called_once()

    @patch("photo_duplicate_finder.gui.messagebox.showwarning")
    def test_requires_at_least_one_keep_selection(self, showwarning):
        with patch("photo_duplicate_finder.gui.messagebox.askyesno") as askyesno:
            keep_selected(
                self.parent,
                self.files,
                set(),
                self.refresh,
                self.next_group,
            )

        self.assertTrue(all(path.exists() for path in self.files))
        self.next_group.assert_not_called()
        askyesno.assert_not_called()
        showwarning.assert_called_once()

    @patch("photo_duplicate_finder.gui.messagebox.askyesno", return_value=False)
    def test_cancel_keeps_all_images(self, askyesno):
        keep_selected(
            self.parent,
            self.files,
            {self.first},
            self.refresh,
            self.next_group,
        )

        self.assertTrue(all(path.exists() for path in self.files))
        self.next_group.assert_not_called()
        askyesno.assert_called_once()
