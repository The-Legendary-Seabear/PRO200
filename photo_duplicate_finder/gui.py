"""Tkinter user interface."""

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def choose_folder(folder_label):
    folder = filedialog.askdirectory(title="Select a Folder Location", mustexist=True)
    folder_label.config(text=folder)
    

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

    search_button = tk.Button(root, text="Search Folder")
    search_button.pack(pady=10)

    root.mainloop()

    if __name__ == "__main__":
        run()

