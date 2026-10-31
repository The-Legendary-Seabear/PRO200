"""Tkinter user interface."""
"""comment"""
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from photo_duplicate_finder.scanner import find_duplicates, find_similar_images
from PIL import Image, ImageTk


THEMES = {
    "light": {
        "background": "#F3F6FB",
        "surface": "#FFFFFF",
        "text": "#172033",
        "muted": "#667085",
        "border": "#E2E8F0",
        "accent": "#4F46E5",
        "accent_hover": "#4338CA",
        "accent_text": "#FFFFFF",
        "button": "#FFFFFF",
        "button_hover": "#F1F5F9",
    },
    "dark": {
        "background": "#111827",
        "surface": "#1F2937",
        "text": "#F3F4F6",
        "muted": "#A0AEC0",
        "border": "#374151",
        "accent": "#818CF8",
        "accent_hover": "#6366F1",
        "accent_text": "#111827",
        "button": "#273449",
        "button_hover": "#34445C",
    },
}


def _style_button(button, theme, primary=False):
    colors = THEMES[theme]
    button.configure(
        bg=colors["accent"] if primary else colors["button"],
        fg=colors["accent_text"] if primary else colors["text"],
        activebackground=colors["accent_hover"] if primary else colors["button_hover"],
        activeforeground=colors["accent_text"] if primary else colors["text"],
        relief="flat",
        bd=0,
        cursor="hand2",
    )


def choose_folder(folder_label):
    folder = filedialog.askdirectory(title="Select a Folder Location", mustexist=True)
    if folder:
        folder_label.config(text=folder)

def search_folder(root, folder_label, include_subfolders, theme="light"):
    folder = folder_label.cget("text")

    if folder == "No folder selected":
        messagebox.showwarning("No Folder", "Please select a folder first.")
        return

    #duplicates = find_duplicates(folder)
    duplicates = find_duplicates(folder, include_subfolders.get())
    similar_images = find_similar_images(folder)
    #display_duplicate_photos(root, duplicates, similar_images)
    display_duplicate_photos(root, duplicates, similar_images, theme)

    #display_similar_images(root, similar_images)


IMAGES_PER_ROW = 4


#def display_duplicate_photos(root, duplicates, similar_images):
def display_duplicate_photos(root, duplicates,similar_images, theme="light"):
    colors = THEMES[theme]
    popup = tk.Toplevel(root)
    popup.title("Duplicate Photos")
    popup.geometry("920x680")
    popup.minsize(640, 480)
    popup.configure(bg=colors["background"])

    if not duplicates:
        
        display_similar_images(root, similar_images)
        tk.Label(
            popup,
            text="No duplicate photos found.",
            font=("Segoe UI", 13),
            bg=colors["background"],
            fg=colors["text"],
        ).pack(expand=True)
        return

    groups = [list(files) for files in duplicates.values()]
    state = {"index": 0}

    heading = tk.Frame(popup, bg=colors["background"])
    heading.pack(fill="x", padx=28, pady=(24, 16))
    tk.Label(
        heading,
        text="Review duplicate photos",
        font=("Segoe UI", 20, "bold"),
        bg=colors["background"],
        fg=colors["text"],
    ).pack(anchor="w")
    set_label = tk.Label(
        heading,
        font=("Segoe UI", 10),
        bg=colors["background"],
        fg=colors["muted"],
    )
    set_label.pack(anchor="w", pady=(5, 0))

    content_frame = tk.Frame(popup, bg=colors["background"])
    content_frame.pack(fill="both", expand=True, padx=20)

    content_canvas = tk.Canvas(
        content_frame,
        bg=colors["background"],
        highlightthickness=0,
        borderwidth=0,
    )
    vertical_scrollbar = tk.Scrollbar(
        content_frame,
        orient="vertical",
        command=content_canvas.yview,
    )
    vertical_scrollbar.configure(
        bg=colors["button"],
        activebackground=colors["accent"],
        troughcolor=colors["background"],
        relief="flat",
        bd=0,
    )
    content_canvas.configure(
        yscrollcommand=vertical_scrollbar.set,
    )

    content_canvas.grid(row=0, column=0, sticky="nsew")
    vertical_scrollbar.grid(row=0, column=1, sticky="ns")
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    group_frame = tk.Frame(content_canvas, bg=colors["background"])
    group_window = content_canvas.create_window(
        (0, 0),
        window=group_frame,
        anchor="n",
    )
    content_canvas.bind(
        "<Configure>",
        lambda event: content_canvas.coords(
            group_window,
            event.width / 2,
            0,
        ),
    )
    group_frame.bind(
        "<Configure>",
        lambda _event: content_canvas.configure(
            scrollregion=content_canvas.bbox("all")
        ),
    )

    next_button = tk.Button(popup, text="Next")
    next_button.configure(
        font=("Segoe UI", 10, "bold"),
        padx=20,
        pady=10,
    )
    _style_button(next_button, theme, primary=True)
    next_button.pack(anchor="e", padx=28, pady=20)

    def show_current_group():
        for widget in group_frame.winfo_children():
            widget.destroy()

        index = state["index"]
        if index == len(groups) - 1:
            next_button.config(text="Finish")
        else:
            next_button.config(text="Next")

        set_label.config(
            text=f"Set {index + 1} of {len(groups)}"
            "  ·  Select which photos to keep or delete"
        )
        display_duplicate_group(
            group_frame,
            groups[index],
            show_next_group,
            theme=theme,
        )

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

def display_duplicate_group(
    parent,
    files,
    next_group,
    keep_files=None,
    delete_files=None,
    theme="light",
):
    colors = THEMES[theme]
    if keep_files is None:
        keep_files = set()
    if delete_files is None:
        delete_files = set()

    def refresh():
        for widget in parent.winfo_children():
            widget.destroy()
        display_duplicate_group(
            parent,
            files,
            next_group,
            keep_files,
            delete_files,
            theme,
        )

    duplicate_frame = tk.Frame(parent, bg=colors["background"])
    duplicate_frame.pack(pady=(0, 15))

    if len(files) < 2:
        message = tk.Label(
            duplicate_frame,
            text="No duplicates left in this set. Click Next to continue.",
            font=("Segoe UI", 11),
            bg=colors["background"],
            fg=colors["muted"],
        )
        message.grid(row=0, column=0, columnspan=IMAGES_PER_ROW, pady=20)

    for position, file_path in enumerate(files):
        row = (position // IMAGES_PER_ROW) * 5 + 1
        column = position % IMAGES_PER_ROW

        path_label = tk.Label(
            duplicate_frame,
            text=str(file_path),
            font=("Segoe UI", 8),
            bg=colors["background"],
            fg=colors["muted"],
            wraplength=170,
            justify="center",
        )
        path_label.grid(row=row, column=column, padx=10)

        image = Image.open(file_path)
        image.thumbnail((150, 150))

        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(
            duplicate_frame,
            image=photo,
            bg=colors["surface"],
            width=160,
            height=160,
            anchor="center",
        )
        image_label.image = photo
        image_label.grid(row=row + 1, column=column, padx=10)

        name_label = tk.Label(
            duplicate_frame,
            text=file_path.name,
            font=("Segoe UI", 9, "bold"),
            bg=colors["background"],
            fg=colors["text"],
            wraplength=170,
            justify="center",
        )
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
            font=("Segoe UI", 9),
            bg=colors["background"],
            fg=colors["text"],
            activebackground=colors["background"],
            activeforeground=colors["text"],
            selectcolor=colors["surface"],
            cursor="hand2",
        )
        keep_checkbutton.grid(row=row + 3, column=column, padx=10)

        delete_checkbutton = tk.Checkbutton(
            duplicate_frame,
            text="Delete",
            variable=delete_var,
            command=update_delete_selection,
            font=("Segoe UI", 9),
            bg=colors["background"],
            fg=colors["text"],
            activebackground=colors["background"],
            activeforeground=colors["text"],
            selectcolor=colors["surface"],
            cursor="hand2",
        )
        delete_checkbutton.grid(
            row=row + 4, column=column, padx=10, pady=(0, 15)
        )

    if len(files) >= 2:
        action_frame = tk.Frame(parent, bg=colors["background"])
        action_frame.pack(pady=10)

        delete_button = tk.Button(
            action_frame,
            text="Delete selected",
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=9,
            command=lambda: delete_selected(
                parent, files, delete_files, refresh, next_group
            ),
        )
        _style_button(delete_button, theme)
        delete_button.pack(side="left", padx=5)

        keep_button = tk.Button(
            action_frame,
            text="Keep selected",
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=9,
            command=lambda: keep_selected(
                parent, files, keep_files, refresh, next_group
            ),
        )
        _style_button(keep_button, theme, primary=True)
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
    root.geometry("820x590")
    root.minsize(640, 500)
    theme_state = {"name": "light"}
    colors = THEMES["light"]
    root.configure(bg=colors["background"])

    outer = tk.Frame(root, bg=colors["background"])
    outer.pack(fill="both", expand=True, padx=48, pady=30)

    header = tk.Frame(outer, bg=colors["background"])
    header.pack(fill="x", pady=(0, 28))
    brand = tk.Frame(header, bg=colors["background"])
    brand.pack(side="left")
    eyebrow = tk.Label(
        brand,
        text="PHOTO TOOLKIT",
        font=("Segoe UI", 9, "bold"),
        bg=colors["background"],
        fg=colors["accent"],
    )
    eyebrow.pack(anchor="w")
    title = tk.Label(
        brand,
        text="Photo Duplicate Finder",
        font=("Segoe UI", 22, "bold"),
        bg=colors["background"],
        fg=colors["text"],
    )
    title.pack(anchor="w", pady=(4, 0))

    theme_button = tk.Button(
        header,
        text="Dark mode",
        font=("Segoe UI", 9, "bold"),
        padx=14,
        pady=9,
    )
    _style_button(theme_button, "light")
    theme_button.pack(side="right", anchor="n")

    card = tk.Frame(
        outer,
        bg=colors["surface"],
        highlightbackground=colors["border"],
        highlightthickness=1,
        padx=28,
        pady=26,
    )
    card.pack(fill="both", expand=True)
    section_title = tk.Label(
        card,
        text="Find duplicate photos",
        font=("Segoe UI", 16, "bold"),
        bg=colors["surface"],
        fg=colors["text"],
    )
    section_title.pack(anchor="w")
    description = tk.Label(
        card,
        text="Scan a folder for identical images, then decide which copies to keep.",
        font=("Segoe UI", 10),
        bg=colors["surface"],
        fg=colors["muted"],
    )
    description.pack(anchor="w", pady=(5, 22))
    folder_heading = tk.Label(
        card,
        text="FOLDER TO SCAN",
        font=("Segoe UI", 9, "bold"),
        bg=colors["surface"],
        fg=colors["muted"],
    )
    folder_heading.pack(anchor="w", pady=(0, 8))

    folder_row = tk.Frame(card, bg=colors["surface"])
    folder_row.pack(fill="x")
    folder_label = tk.Label(
        folder_row,
        text="No folder selected",
        font=("Segoe UI", 10),
        anchor="w",
        padx=12,
        pady=12,
        highlightthickness=1,
        wraplength=480,
        bg=colors["surface"],
        fg=colors["muted"],
        highlightbackground=colors["border"],
    )
    folder_label.pack(side="left", fill="x", expand=True, padx=(0, 10))
    choose_button = tk.Button(
        folder_row,
        text="Browse...",
        font=("Segoe UI", 9, "bold"),
        padx=16,
        pady=11,
        command=lambda: choose_folder(folder_label),
    )
    _style_button(choose_button, "light")
    choose_button.pack(side="right")

    include_subfolders = tk.BooleanVar(value=False)
    subfolder_check = tk.Checkbutton(
        card,
        text="Include subfolders",
        variable=include_subfolders,
        font=("Segoe UI", 9),
        bg=colors["surface"],
        fg=colors["text"],
        activebackground=colors["surface"],
        activeforeground=colors["text"],
        selectcolor=colors["background"],
        cursor="hand2",
    )
    subfolder_check.pack(anchor="w", pady=(14, 0))
    search_button = tk.Button(
        card,
        text="Scan for duplicates",
        font=("Segoe UI", 10, "bold"),
        padx=20,
        pady=12,
        command=lambda: search_folder(
            root,
            folder_label,
            include_subfolders,
            theme_state["name"],
        ),
    )
    _style_button(search_button, "light", primary=True)
    search_button.pack(anchor="w", pady=(20, 12))
    status_label = tk.Label(
        card,
        text="Your photos stay on your device.",
        font=("Segoe UI", 9),
        bg=colors["surface"],
        fg=colors["muted"],
    )
    status_label.pack(anchor="w")

    def toggle_theme():
        theme = "dark" if theme_state["name"] == "light" else "light"
        theme_state["name"] = theme
        colors = THEMES[theme]
        root.configure(bg=colors["background"])
        outer.configure(bg=colors["background"])
        header.configure(bg=colors["background"])
        brand.configure(bg=colors["background"])
        eyebrow.configure(bg=colors["background"], fg=colors["accent"])
        title.configure(bg=colors["background"], fg=colors["text"])
        card.configure(
            bg=colors["surface"],
            highlightbackground=colors["border"],
        )
        section_title.configure(bg=colors["surface"], fg=colors["text"])
        description.configure(bg=colors["surface"], fg=colors["muted"])
        folder_heading.configure(bg=colors["surface"], fg=colors["muted"])
        folder_row.configure(bg=colors["surface"])
        folder_label.configure(
            bg=colors["surface"],
            fg=colors["muted"]
            if folder_label.cget("text") == "No folder selected"
            else colors["text"],
            highlightbackground=colors["border"],
        )
        subfolder_check.configure(
            bg=colors["surface"],
            fg=colors["text"],
            activebackground=colors["surface"],
            activeforeground=colors["text"],
            selectcolor=colors["background"],
        )
        status_label.configure(bg=colors["surface"], fg=colors["muted"])
        _style_button(choose_button, theme)
        _style_button(search_button, theme, primary=True)
        _style_button(theme_button, theme)
        theme_button.configure(
            text="Light mode" if theme == "dark" else "Dark mode"
        )

    theme_button.configure(command=toggle_theme)

    root.mainloop()


if __name__ == "__main__":
    run()
