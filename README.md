# Photo Duplicate Finder

## Project Description

Photo Duplicate Finder is a Python application designed to help users find duplicate and visually similar images inside a selected folder.

The program will use two main methods to detect duplicates:

- **File hashing** to identify images that are exact duplicates.
- **Image comparison** to identify images that look the same or very similar even if the files are not identical.

The application will provide a simple graphical interface where the user can select a folder, scan its images, review detected duplicates, and decide which files they want to keep or remove.

## Team Member(s)

- Alex Kohn
- Christopher Munson

## Technologies Being Used

- **Python** – Main programming language for the application.
- **Tkinter** – Used to create the graphical user interface.
- **OpenCV** – Used for image processing and comparing images.
- **Pillow (PIL)** – Used for loading, resizing, and displaying images.
- **ImageHash** – Used to create perceptual hashes for detecting visually similar images.
- **hashlib** – Built-in Python library used to create file hashes for finding exact duplicate files.
- **pathlib / os** – Used to navigate folders and work with files on the user's computer.

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

Run the main Python file:

```bash
python main.py
```

Once the program starts, select a folder containing images and begin the duplicate scan.
