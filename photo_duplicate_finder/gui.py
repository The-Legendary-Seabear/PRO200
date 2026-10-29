"""Tkinter user interface."""
"""comment"""
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from photo_duplicate_finder.scanner import find_duplicates, find_similar_images
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
    similar_images = find_similar_images(folder)
    display_duplicate_photos(root, duplicates, similar_images)

    #display_similar_images(root, similar_images)

IMAGES_PER_ROW = 4


def display_duplicate_photos(root, duplicates, similar_images):
    popup = tk.Toplevel(root)
    popup.title("Duplicate Photos")
    popup.geometry("800x600")

    if not duplicates:
        label = tk.Label(popup, text="No duplicate photos found.")
        label.pack(pady=20)
        display_similar_images(root, similar_images)
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
            display_similar_images(root, similar_images)

    next_button.config(command=show_next_group)
    show_current_group()

def display_similar_images(root, similars):
    popup = tk.Toplevel(root)
    popup.title("Similar Photos")
    popup.geometry("800x600")
    if not similars:
            label = tk.Label(popup, text="No similar photos found.")
            label.pack(pady=20)
            return
    
    groups = [[file1, file2]
    for file1, file2, difference in similars
]
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
        set_label.config(text=f"Similar image pair {index + 1} of {len(groups)}")
        if index == len(groups) - 1:
             next_button.config(text="Finish")
        else:
            next_button.config(text="Next")
    
        display_similar_group(group_frame, groups[index])
    
    def show_next_group():
        if state["index"] < len(groups) - 1:
            state["index"] += 1
            show_current_group()
        else:
            messagebox.showinfo(
                "Done",
                "You have reviewed all similar sets.",
                parent=popup,
            )
            popup.destroy()
    
    next_button.config(command=show_next_group)
    show_current_group()

def display_similar_group(parent, files):
    similar_frame = tk.Frame(parent)
    similar_frame.pack(pady=15)

    for position, file_path in enumerate(files):
        image = Image.open(file_path)
        image.thumbnail((150, 150))

        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(similar_frame, image=photo)
        image_label.image = photo
        image_label.grid(row=0, column=position, padx=15)

        name_label = tk.Label(
            similar_frame,
            text=file_path.name
        )
        name_label.grid(row=1, column=position, padx=15)

def display_duplicate_group(parent, files, next_group):
    def refresh():
        for widget in parent.winfo_children():
            widget.destroy()
        display_duplicate_group(parent, files, next_group)

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

        keep_button = tk.Button(
            duplicate_frame,
            text="Keep this image",
            command=lambda path=file_path: keep_photo(
                parent, files, path, refresh, next_group
            ),
        )
        keep_button.grid(row=row + 2, column=column, padx=10, pady=(0, 15))


def keep_photo(parent, files, file_path, refresh, next_group):
    duplicates = [path for path in files if path != file_path]
    if not duplicates:
        next_group()
        return

    confirmed = messagebox.askyesno(
        "Keep this image",
        f"Keep {file_path.name} and permanently delete "
        f"{len(duplicates)} other {'copy' if len(duplicates) == 1 else 'copies'}?",
        parent=parent.winfo_toplevel(),
    )
    if not confirmed:
        return

    failed_deletions = []
    for duplicate in duplicates:
        try:
            duplicate.unlink()
        except OSError as error:
            failed_deletions.append((duplicate, error))

    if failed_deletions:
        files[:] = [file_path] + [path for path, _ in failed_deletions]
        messagebox.showerror(
            "Could not delete all duplicate photos",
            "\n".join(f"{path}: {error}" for path, error in failed_deletions),
            parent=parent.winfo_toplevel(),
        )
        refresh()
        return

    files[:] = [file_path]
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

    search_button = tk.Button(root, text="Search Folder", command=lambda: search_folder(root, folder_label))
    search_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    run()
