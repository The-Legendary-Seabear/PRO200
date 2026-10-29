"""Tkinter user interface."""
"""comment"""
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from photo_duplicate_finder.scanner import find_duplicates
from PIL import Image, ImageTk

def choose_folder(folder_label):
    folder = filedialog.askdirectory(title="Select a Folder Location", mustexist=True)
    if folder:
        folder_label.config(text=folder)

def search_folder(root, folder_label, include_subfolders):
    folder = folder_label.cget("text")

    if folder == "No folder selected":
        messagebox.showwarning("No Folder", "Please select a folder first.")
        return

    duplicates = find_duplicates(folder, include_subfolders.get())

    display_duplicate_photos(root, duplicates)

IMAGES_PER_ROW = 4


def display_duplicate_photos(root, duplicates):
    popup = tk.Toplevel(root)
    popup.title("Duplicate Photos")
    popup.geometry("800x600")

    if not duplicates:
        label = tk.Label(popup, text="No duplicate photos found.")
        label.pack(pady=20)
        return

    groups = [list(files) for files in duplicates.values()]
    state = {"index": 0}

    set_label = tk.Label(popup, font=("Arial", 14))
    set_label.pack(pady=10)

    content_frame = tk.Frame(popup)
    content_frame.pack(fill="both", expand=True)

    content_canvas = tk.Canvas(content_frame)
    vertical_scrollbar = tk.Scrollbar(
        content_frame,
        orient="vertical",
        command=content_canvas.yview,
    )
    horizontal_scrollbar = tk.Scrollbar(
        content_frame,
        orient="horizontal",
        command=content_canvas.xview,
    )
    content_canvas.configure(
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set,
    )

    content_canvas.grid(row=0, column=0, sticky="nsew")
    vertical_scrollbar.grid(row=0, column=1, sticky="ns")
    horizontal_scrollbar.grid(row=1, column=0, sticky="ew")
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    group_frame = tk.Frame(content_canvas)
    content_canvas.create_window((0, 0), window=group_frame, anchor="nw")
    group_frame.bind(
        "<Configure>",
        lambda _event: content_canvas.configure(
            scrollregion=content_canvas.bbox("all")
        ),
    )

    next_button = tk.Button(popup, text="Next")
    next_button.pack(pady=10)

    def show_current_group():
        for widget in group_frame.winfo_children():
            widget.destroy()

        index = state["index"]
        set_label.config(text=f"Duplicate set {index + 1} of {len(groups)}")
        if index == len(groups) - 1:
            next_button.config(text="Finish")
        else:
            next_button.config(text="Next")

        display_duplicate_group(group_frame, groups[index], show_next_group)

    def show_next_group():
        if state["index"] < len(groups) - 1:
            state["index"] += 1
            show_current_group()
        else:
            messagebox.showinfo(
                "Done",
                "You have reviewed all duplicate sets.",
                parent=popup,
            )
            popup.destroy()

    next_button.config(command=show_next_group)
    show_current_group()


def display_duplicate_group(parent, files, next_group, keep_files=None, delete_files=None):
    if keep_files is None:
        keep_files = set()
    if delete_files is None:
        delete_files = set()

    def refresh():
        for widget in parent.winfo_children():
            widget.destroy()
        display_duplicate_group(parent, files, next_group, keep_files, delete_files)

    duplicate_frame = tk.Frame(parent)
    duplicate_frame.pack(pady=(0, 15))

    if len(files) < 2:
        message = tk.Label(
            duplicate_frame,
            text="No duplicates left in this set. Click Next to continue.",
        )
        message.grid(row=0, column=0, columnspan=IMAGES_PER_ROW, pady=20)

    for position, file_path in enumerate(files):
        row = (position // IMAGES_PER_ROW) * 5 + 1
        column = position % IMAGES_PER_ROW

        path_label = tk.Label(
            duplicate_frame,
            text=str(file_path),
            wraplength=170,
            justify="center",
        )
        path_label.grid(row=row, column=column, padx=10)

        image = Image.open(file_path)
        image.thumbnail((150, 150))

        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(duplicate_frame, image=photo)
        image_label.image = photo
        image_label.grid(row=row + 1, column=column, padx=10)

        name_label = tk.Label(duplicate_frame, text=file_path.name)
        name_label.grid(row=row + 2, column=column, padx=10)

        keep_var = tk.BooleanVar(value=file_path in keep_files)
        delete_var = tk.BooleanVar(value=file_path in delete_files)

        def update_keep_selection(
            path=file_path,
            variable=keep_var,
            other_variable=delete_var,
        ):
            if variable.get():
                other_variable.set(False)
                delete_files.discard(path)
                keep_files.add(path)
            else:
                keep_files.discard(path)

        def update_delete_selection(
            path=file_path,
            variable=delete_var,
            other_variable=keep_var,
        ):
            if variable.get():
                other_variable.set(False)
                keep_files.discard(path)
                delete_files.add(path)
            else:
                delete_files.discard(path)

        keep_checkbutton = tk.Checkbutton(
            duplicate_frame,
            text="Keep",
            variable=keep_var,
            command=update_keep_selection,
        )
        keep_checkbutton.grid(row=row + 3, column=column, padx=10)

        delete_checkbutton = tk.Checkbutton(
            duplicate_frame,
            text="Delete",
            variable=delete_var,
            command=update_delete_selection,
        )
        delete_checkbutton.grid(
            row=row + 4, column=column, padx=10, pady=(0, 15)
        )

    if len(files) >= 2:
        action_frame = tk.Frame(parent)
        action_frame.pack(pady=10)

        delete_button = tk.Button(
            action_frame,
            text="Delete selected",
            command=lambda: delete_selected(
                parent, files, delete_files, refresh, next_group
            ),
        )
        delete_button.pack(side="left", padx=5)

        keep_button = tk.Button(
            action_frame,
            text="Keep selected",
            command=lambda: keep_selected(
                parent, files, keep_files, refresh, next_group
            ),
        )
        keep_button.pack(side="left", padx=5)


def delete_selected(parent, files, delete_files, refresh, next_group):
    delete_files = {path for path in files if path in delete_files}
    delete_marked_files(
        parent,
        files,
        delete_files,
        "Delete selected images",
        refresh,
        next_group,
    )


def keep_selected(parent, files, keep_files, refresh, next_group):
    keep_files = {path for path in files if path in keep_files}
    if not keep_files:
        messagebox.showwarning(
            "Choose images to keep",
            "Check Keep under the images you want to save first.",
            parent=parent.winfo_toplevel(),
        )
        return

    delete_marked_files(
        parent,
        files,
        set(files) - keep_files,
        "Keep selected images",
        refresh,
        next_group,
    )


def delete_marked_files(parent, files, files_to_delete, action, refresh, next_group):
    if not files_to_delete:
        messagebox.showinfo(
            "Nothing to delete",
            "There are no images to delete.",
            parent=parent.winfo_toplevel(),
        )
        return

    confirmed = messagebox.askyesno(
        action,
        f"Permanently delete {len(files_to_delete)} "
        f"{'image' if len(files_to_delete) == 1 else 'images'}?",
        parent=parent.winfo_toplevel(),
    )
    if not confirmed:
        return

    failed_deletions = []
    for file_path in files_to_delete:
        try:
            file_path.unlink()
        except OSError as error:
            failed_deletions.append((file_path, error))

    if failed_deletions:
        failed_paths = {path for path, _ in failed_deletions}
        files[:] = [
            path
            for path in files
            if path not in files_to_delete or path in failed_paths
        ]
        messagebox.showerror(
            "Could not delete all images",
            "\n".join(f"{path}: {error}" for path, error in failed_deletions),
            parent=parent.winfo_toplevel(),
        )
        refresh()
        return

    files[:] = [path for path in files if path not in files_to_delete]
    next_group()

def run() -> None:
    """Create and display the application window."""
    root = tk.Tk()
    root.title("Photo Duplicate Finder")
    root.geometry("700x450")

    title = tk.Label(root, text="Photo Duplicate Finder", font=("Arial", 18))
    title.pack(pady=24)

    prompt = tk.Label(root, text="Choose a folder to scan for duplicate images.")
    prompt.pack()

    folder_label = tk.Label(root,text="No folder selected")
    folder_label.pack(pady=10)

    choose_button = tk.Button(root,text="Choose Folder",command=lambda: choose_folder(folder_label))
    choose_button.pack(pady=10)

    include_subfolders = tk.BooleanVar(value=False)
    subfolder_check = tk.Checkbutton(root, text="Include subfolders", variable=include_subfolders)
    subfolder_check.pack(pady=5)

    search_button = tk.Button(root, text="Search Folder", command=lambda: search_folder(root, folder_label, include_subfolders))
    search_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    run()
