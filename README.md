# Photo Duplicate Finder

## Project Description

Photo Duplicate Finder is a Python application designed to help users find duplicate and visually similar images inside a selected folder.

The program will use two main methods to detect duplicates:

- **File hashing** to identify images that are exact duplicates.
- **Image comparison** to identify images that look the same or very similar even if the files are not identical.

The application provides a simple graphical interface where the user can select a folder and scan its images. Each duplicate group includes a button to keep the first listed photo and permanently delete the other copies, after confirmation.

## Team Member(s)

- Alex Kohn
- Cole Lowery
- Christopher Munson
- Nicholas Alabre

## Technologies Being Used

- **Python** - Main programming language for the application.
- **Tkinter** - Used to create the graphical user interface.
- **OpenCV** - Used for image processing and comparing images.
- **Pillow (PIL)** - Used for loading, resizing, and displaying images.
- **ImageHash** - Used to create perceptual hashes for detecting visually similar images.
- **hashlib** - Built-in Python library used to create file hashes for finding exact duplicate files.
- **pathlib / os** - Used to navigate folders and work with files on the user's computer.

## Project Structure

```text
PRO200/
├── main.py                       # Application entry point
├── photo_duplicate_finder/
│   ├── __init__.py
│   ├── app.py                    # Application startup and coordination
│   ├── gui.py                    # Tkinter user interface
│   ├── hashing.py                # Exact and perceptual image hashing
│   └── scanner.py                # Folder traversal and image discovery
├── tests/                        # Automated tests
└── README.md
```

## Basic Setup and Installation

### 1. Install Python

Install Python 3 if it is not already installed.

Verify the installation with:

```bash
python --version
```

### 2. Clone or Download the Project

Clone the repository:

```bash
git clone <repository-url>
```

Then enter the project folder:

```bash
cd photo-duplicate-finder
```

### 3. Install Required Libraries

Install the required Python packages:

```bash
pip install opencv-python pillow ImageHash
```

Tkinter, hashlib, pathlib, and os are included with standard Python installations.

### 4. Run the Application

From the project folder, run:

```bash
python main.py
```

Duplicate groups are detected by exact file hash. In the results window, use a
group's **Keep ..., delete other copies** button to remove all but the first
listed file. Deletion is permanent and requires confirmation.
