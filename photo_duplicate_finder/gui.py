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

def search_folder(root, folder_label):
    folder = folder_label.cget("text")

    if folder == "No folder selected":
        messagebox.showwarning("No Folder", "Please select a folder first.")
        return

    duplicates = find_duplicates(folder)

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

    group_frame = tk.Frame(popup)
    group_frame.pack(fill="both", expand=True)

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

        display_duplicate_group(group_frame, groups[index], show_current_group)

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


def display_duplicate_group(parent, files, refresh):
    duplicate_frame = tk.Frame(parent)
    duplicate_frame.pack(pady=(0, 15))

    if len(files) < 2:
        message = tk.Label(
            duplicate_frame,
            text="No duplicates left in this set. Click Next to continue.",
        )
        message.grid(row=0, column=0, columnspan=IMAGES_PER_ROW, pady=20)

    for position, file_path in enumerate(files):
        row = (position // IMAGES_PER_ROW) * 3 + 1
        column = position % IMAGES_PER_ROW

        image = Image.open(file_path)
        image.thumbnail((150, 150))

        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(duplicate_frame, image=photo)
        image_label.image = photo
        image_label.grid(row=row, column=column, padx=10)

        name_label = tk.Label(duplicate_frame, text=file_path.name)
        name_label.grid(row=row + 1, column=column, padx=10)

        delete_button = tk.Button(
            duplicate_frame,
            text="Delete",
            command=lambda path=file_path: delete_photo(
                parent, files, path, refresh
            ),
        )
        delete_button.grid(row=row + 2, column=column, padx=10, pady=(0, 15))


def delete_photo(parent, files, file_path, refresh):
    confirmed = messagebox.askyesno(
        "Delete photo",
        f"Permanently delete {file_path.name}?",
        parent=parent.winfo_toplevel(),
    )
    if not confirmed:
        return

    try:
        file_path.unlink()
    except OSError as error:
        messagebox.showerror(
            "Could not delete photo",
            f"{file_path}: {error}",
            parent=parent.winfo_toplevel(),
        )
        return

    files.remove(file_path)
    refresh()

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

    search_button = tk.Button(root, text="Search Folder", command=lambda: search_folder(root, folder_label))
    search_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    run()
