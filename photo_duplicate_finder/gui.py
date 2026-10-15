"""Tkinter user interface."""

import tkinter as tk


def run() -> None:
    """Create and display the application window."""
    root = tk.Tk()
    root.title("Photo Duplicate Finder")
    root.geometry("700x450")

    title = tk.Label(root, text="Photo Duplicate Finder", font=("Arial", 18))
    title.pack(pady=24)

    prompt = tk.Label(root, text="Choose a folder to scan for duplicate images.")
    prompt.pack()

    root.mainloop()
