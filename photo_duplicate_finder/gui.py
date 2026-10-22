"""Tkinter user interface."""

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

def display_duplicate_photos(root, duplicates):
    popup = tk.Toplevel(root)
    popup.title("Duplicate Photos")
    popup.geometry("800x600")

    if not duplicates:
        label = tk.Label(popup, text="No duplicate photos found.")
        label.pack(pady=20)
        return

    for file_hash, files in duplicates.items():
        for file_path in files:
            image = Image.open(file_path)
            image.thumbnail((150, 150))

            photo = ImageTk.PhotoImage(image)

            image_label = tk.Label(popup, image=photo)
            image_label.image = photo
            image_label.pack()

            name_label = tk.Label(
                popup,
                text=file_path.name
            )
            name_label.pack(pady=(0, 15))

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

