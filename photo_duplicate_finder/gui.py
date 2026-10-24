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

def display_duplicate_photos(root, duplicates):
    popup = tk.Toplevel(root)
    popup.title("Duplicate Photos")
    popup.geometry("800x600")

    if not duplicates:
        label = tk.Label(popup, text="No duplicate photos found.")
        label.pack(pady=20)
        return

    results_canvas = tk.Canvas(popup, highlightthickness=0)
    scrollbar = tk.Scrollbar(popup, orient="vertical", command=results_canvas.yview)
    horizontal_scrollbar = tk.Scrollbar(
        popup,
        orient="horizontal",
        command=results_canvas.xview,
    )
    results_canvas.configure(
        yscrollcommand=scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set,
    )

    horizontal_scrollbar.pack(side="bottom", fill="x")
    scrollbar.pack(side="right", fill="y")
    results_canvas.pack(side="left", fill="both", expand=True)

    results_frame = tk.Frame(results_canvas)
    results_window = results_canvas.create_window(
        (0, 0),
        window=results_frame,
        anchor="nw",
    )

    results_frame.bind(
        "<Configure>",
        lambda event: results_canvas.configure(
            scrollregion=results_canvas.bbox("all")
        ),
    )

    for files in duplicates.values():
        display_duplicate_group(results_frame, files)


def display_duplicate_group(parent, files):
    duplicate_frame = tk.Frame(parent)
    duplicate_frame.pack(pady=(0, 15))

    for column, file_path in enumerate(files):
        image = Image.open(file_path)
        image.thumbnail((150, 150))

        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(duplicate_frame, image=photo)
        image_label.image = photo
        image_label.grid(row=0, column=column, padx=10)

        name_label = tk.Label(duplicate_frame, text=file_path.name)
        name_label.grid(row=1, column=column, padx=10, pady=(0, 15))

    delete_button = tk.Button(
        duplicate_frame,
        text=f"Keep {files[0].name}, delete other copies",
        command=lambda: delete_duplicate_group(parent, files, duplicate_frame),
    )
    delete_button.grid(row=2, column=0, columnspan=len(files), pady=(0, 10))


def delete_duplicate_group(parent, files, duplicate_frame):
    kept_file = files[0]
    files_to_delete = files[1:]
    confirmed = messagebox.askyesno(
        "Delete duplicate photos",
        f"Keep {kept_file.name} and permanently delete "
        f"{len(files_to_delete)} duplicate photo(s)?",
        parent=parent.winfo_toplevel(),
    )
    if not confirmed:
        return

    failed_files = []
    for file_path in files_to_delete:
        try:
            file_path.unlink()
        except OSError as error:
            failed_files.append((file_path, error))

    if failed_files:
        duplicate_frame.destroy()
        display_duplicate_group(
            parent,
            [kept_file, *(file_path for file_path, _ in failed_files)],
        )
        failures = "\n".join(
            f"{file_path}: {error}" for file_path, error in failed_files
        )
        messagebox.showerror(
            "Could not delete all duplicates",
            f"Some files were deleted, but these could not be removed:\n{failures}",
            parent=parent.winfo_toplevel(),
        )
        return

    duplicate_frame.destroy()
    messagebox.showinfo(
        "Duplicates deleted",
        f"Kept {kept_file.name} and deleted {len(files_to_delete)} duplicate "
        f"photo(s).",
        parent=parent.winfo_toplevel(),
    )

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
