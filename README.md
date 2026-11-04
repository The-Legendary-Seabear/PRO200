# Photo Duplicate Finder

## Project Description

Photo Duplicate Finder is a Python desktop application designed to help users identify and manage exact duplicate and visually similar images within their photo collections.

The application helps users organize their photos, remove unnecessary copies, and free up storage space without manually comparing every image.

It uses two detection methods:

- **SHA-256 File Hashing:** Identifies files that are byte-for-byte identical, regardless of their filenames.
- **Perceptual Hashing (pHash):** Identifies images with similar visual characteristics, even when their file contents differ.

Users can scan a single folder or compare the combined contents of two folders. The application also supports optional subfolder scanning.

Detected images are displayed in review windows with thumbnails, filenames, and Keep/Delete controls. Users can select which images to preserve or permanently delete after confirmation.

## Team Members

- Alex Kohn
- Cole Lowery
- Christopher Munson
- Nicholas Alabre

## Features

- **Exact Duplicate Detection:** Find identical image files using SHA-256 hashing.
- **Similar Image Detection:** Identify visually similar images using perceptual hashing.
- **Single-Folder Scanning:** Search a selected folder for duplicate and similar images.
- **Two-Folder Comparison:** Search the combined contents of two selected folders, including duplicates within either folder and across both folders.
- **Subfolder Support:** Optionally include nested folders during scanning.
- **Image Previews:** View thumbnails and filenames of detected images.
- **File Management:** Select images to keep or delete, with confirmation before deletion.
- **Light and Dark Modes:** Switch between interface themes.
- **Group Navigation:** Review detected duplicate groups and similar-image pairs using Next and Finish controls.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Primary programming language |
| Tkinter | Desktop graphical user interface |
| Pillow (PIL) | Loading, resizing, and displaying images |
| ImageHash | Perceptual hashing for visually similar image detection |
| hashlib | SHA-256 hashing for exact duplicate detection |
| pathlib | Folder traversal and file management |
| Git and GitHub | Version control and team collaboration |
| Visual Studio Code | Development environment |

## Project Structure

```text
PRO200/
├── .gitignore
├── main.py
├── photo_duplicate_finder/
│   ├── __init__.py
│   ├── app.py
│   ├── gui.py
│   ├── hashing.py
│   └── scanner.py
├── tests/
└── README.md
```

## Setup and Installation

### 1. Install Python

Install Python 3 if it is not already installed.

Verify the installation:

```bash
python --version
```

Tkinter must also be available in the selected Python installation.

### 2. Clone the Repository

```bash
git clone https://github.com/The-Legendary-Seabear/PRO200.git
cd PRO200
```

### 3. Install Required Libraries

```bash
python -m pip install pillow ImageHash
```

Python's `hashlib` and `pathlib` modules are included in the standard library.

### 4. Run the Application

From the project root directory, execute:

```bash
python main.py
```

## How to Use

### Single-Folder Scanning

1. Launch the application.
2. Select a folder using the Browse button.
3. Optionally enable Include Subfolders.
4. Click Scan for Duplicates.
5. Review exact duplicate images.
6. Use the Keep/Delete controls to manage detected images.
7. Continue to the similar-image review after completing the exact-duplicate review.

### Two-Folder Comparison

1. Click Compare Two Folders.
2. Select Folder A and Folder B.
3. Optionally enable subfolder scanning.
4. Click Compare Folders.
5. Review exact duplicate matches from the combined folders.
6. Continue to visually similar image comparisons.
7. Use the existing image review controls to manage detected matches.

### Image Management

Each reviewed image includes Keep and Delete selection options.

- **Keep Selected:** Preserve the selected images and delete unselected images in the reviewed group.
- **Delete Selected:** Delete only images marked for deletion.
- **Next / Finish:** Navigate between groups or complete the review.

The application requests confirmation before deleting files.

**Warning:** File deletion is permanent in the current implementation and does not move images to the Recycle Bin. Users should review their selections carefully and maintain backups of important photos.

## Current Limitations

- Perceptual hashing provides similarity estimates and may identify images that are visually alike but not actual duplicates.
- Large image collections may require additional processing time.
- The interface does not currently provide a dedicated full-size image preview.
- The application currently supports image files rather than video duplicate detection.

## Future Improvements

- Add full-size image previews and zoom functionality.
- Improve the Keep/Delete interface based on user feedback.
- Add progress indicators during longer scans.
- Improve performance when processing large image collections.
- Support video duplicate detection.
- Improve file recovery and deletion safety.
