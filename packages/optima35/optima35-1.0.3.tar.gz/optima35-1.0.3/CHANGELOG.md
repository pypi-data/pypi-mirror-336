# Changelog

## 1.0.x
### 1.0.3 Patch: Adjusted pyproject.toml (25.03.24)
- Added <4.0 python version

### 1.0.2: Added Classifier (25.02.09)
- Added classifiers in `pyproject.toml` for PyPI.

### 1.0.1: Contribution (25.01.28)
- Added a contribution section in the README for Mr. Finch.

### **1.0.0** Refactoring (25.01.28)
- Added function descriptions for better clarity and maintainability.
- Introduced guidelines for each function, defining objectives and expected behavior.

---

## 0.12.x
### 0.12.2: Bug fixes
- Fixed missing lens in meta data
- Fixed incorrect User Comment, aka, Scanner name

### 0.12.1
- Error in GitVersion.yml file resulted in jump from 6 to 12.

### 0.12.0
- Versioning from pipeline.

---

## 0.7.x
### 0.7.0
- **BREAKING CHANGE:** GPS location must now be provided as a float instead of a string.
- Repo only: Pipline

---

## 0.6.x
### 0.6.8
- Repo only: Pipline

### 0.6.6
- Added function to insert exif data into image file (i.e. without modifying image)

### 0.6.5 / -a
- No breaking changes to backward compatibility yet.
- Updated the `process` function: an image can now be returned in a modified form without saving. It is returned as a Qt image, which is required for the new UI functionality.
- No change from alpha to *stable*

### 0.6.4
- Released a stable-ish version to ensure compatibility with the current GUI in OptimaLab35 (v0.1.0).
- This version serves as a baseline before potential breaking changes in future updates.

### 0.6.3-a2
- Adding __version__ to `__init__.py` so version is automaticly updated in program as well as pypi.

### 0.6.3-a1
- Adding postfix a to indicate alpha version, making it clear that it is in an early state

### 0.6.2
- Version on pypi.
- .1 and .2 have no change, but had to republish the file, which required to increase the version number.

### 0.6.0
- Working on to Publish on pypi
- Renaming of files and classes

---

## 0.5.x
### 0.5.0
### **OPTIMA35 0.5.0: Code Cleaning and Preparation for Split**
- Cleaned up the codebase, following **PEP8**, adding indication for only internal functions.
- Refactored the project in preparation for splitting it into **OPTIMA35 (core functionality)** and **UI (graphical and text interfaces)**.
- Moved `image_handler.py` into the `optima` folder/package to integrate it as an essential part of the OPTIMA35 package, rather than just a utility.

### **UI 0.1.0: GUI and TUI Updates**
- Updated **GUI** and **TUI** to work seamlessly with the new **OPTIMA35** class.
- Ensured compatibility with the newly organized codebase in the OPTIMA35 package.

---

## 0.4.x
### 0.4.1: Finished GUI and TUI
- Both **GUI** and **TUI** now fully utilize the `optima35` class for core functionality.
- All planned features are operational and integrated into both interfaces.
- **Next Step**: Bug hunting and optimization.
- The fork `optima-35-tui` has been deleted, as **OPTIMA-35** now includes both **TUI** and **GUI** versions within the same project.

### 0.4.0: Splitting into Classes
- **Code Organization:**
  - Core functionality for **Optima-35** is now refactored into `optima35.py` for better separation of logic and reusability.
  - The **GUI code** is moved to `gui.py` for a cleaner structure and maintainability.
  - The **TUI logic** will be moved into `tui.py`, making it modular and focused.
  - The original TUI fork will be deleted to streamline operations.

- **Main File Enhancements:**
  - `main.py` is now the entry point of the application and determines whether to start the GUI or TUI based on:
    - Operating system.
    - The presence of required dependencies (e.g., PySide for GUI).
    - Command-line arguments (`--tui` flag).

- **Benefits:**
  - Clear separation of concerns between GUI, TUI, and core functionalities.
  - Improved readability, maintainability, and scalability of the project.
  - Easier to test and debug individual components.

---

## 0.3.x
### 0.3.4: Features Finalized
- Core Features Completed:
  - All functions are now available, though minor bugs may exist.
- GUI State:
  - Interface is in a polished state but still needs refinement.

**Implemented Features:**
- Image Processing:
  - Resizing
  - Renaming with order adjustment
  - Grayscale conversion
  - Brightness adjustment
  - Contrast adjustment
- EXIF Management:
  - Copy EXIF data
  - Add custom EXIF information
  - Add GPS data
  - Add date to EXIF
- Watermarking:
  - Watermark functionality is now finalized and no longer experimental.

### 0.3.3: Exif implemented
- New EXIF settings tab in the GUI.
- Popup window for editing EXIF data.
- Added options for:
  - Adding date to EXIF.
  - Adding GPS coordinates to EXIF.

### 0.3.2: New ui
- Major overhaul of the gui
- Adding preview to readme
- All options on the first tab work
  - Watermark still experimentel, font selecting will be added
  - Second tab is for exif control, copy option works already

### 0.3.1: license change
- Changed license from CC BY-NC 4.0 to AGPL-3.0.

### 0.3.0: Qt GUI Transition (PySide6)
- Shifted from a TUI approach to a GUI-based layout.
- Adopted **PySide6** for the GUI and **Qt Designer** for designing layouts.
- Introduced a proof-of-concept UI, and adding own exif does not work
- Watermark is still in testing / alpha
- Original TUI version was forked and is still aviable, currently this branch includes the TUI version until the next minor version change.

---

## 0.2.x
### 0.2.1: Merge from TUI fork
- Ensure watermark is white with black borders.

### 0.2.0
- **Cleaner folder structure**
    - Moving files with classes to different folder to keep project cleaner.

---

## 0.1.x
### 0.1.1
- **Add Original to add Timestamp to Images**
    - Introduced an option to add the original timestamp to images. Some programs use timestamps rather than file names to determine order, also enables a timeline-like organization for images.
- **Improved Font Handling**
    - Instead of terminating the process when a font is not found, the program now skips the operation gracefully.
- **Input Validation**
    - Added checks for input types, including strings, floats, and integers, to enhance robustness.
- **Save Function Optimization**
    - Optimized the save function for cleaner code, partially utilizing ChatGPT-generated suggestions.
- **Code Formatting**
    - Improved code structure and formatting for better readability and maintainability.

### 0.1.0: Core Features Added
- **Images are modified through all selected options without saving, reducing quality degradation and saving local storage.**
- **All core features are available:**
    - Simple TUI including options for selecting:
    - Resize
    - Change EXIF (with options from exif_options.yaml), copy original or leave empty
    - Convert to grayscale
    - Change contrast
    - Change brightness
    - Rename images (numbers are added automatically at the end)
    - Invert image order (so that the first image gets the last number and the last image gets the first; this is useful when the original numbering is reversed, which often happens when scanning 35mm film).
    - Add watermark (**Experimental**, requires the correct font to be installed)
- **Settings via YAML:**
    - At the start of the program, the user is asked to save default values, such as JPG quality, resize options, and more. This way, the settings don't have to be entered at every start. Upon starting, the user is prompted to confirm whether they want to keep the current settings from the settings file.
    - Options for changing EXIF data are saved in exif_options.yaml. Here, you can enter all the models, lenses, etc., you would like to select within the program.

---

## 0.0.x
### 0.0.3: Enhanced Functionality - now useable
- **New Image Modification Functions:**
    - Added support for Grayscale conversion.
    - Introduced Brightness adjustment.
   - Enhanced with Contrast adjustment.
- **New User Selection/Settings Features:**
    - Default values for settings can now be saved, such as:
    - JPEG quality.
    - PNG compression.
    - Additional optimization preferences.
    - Input folder, output folder, and file type are requested for every session.
- **Progress Bar for Image Processing:**
    - Implemented a progress bar to visually track the processing of images.

### 0.0.2: Enhanced Functionality
- **First Functional Features:**
    - Introduced the first operational functions, enabling the program to process images based on user input.
- **User Interaction:**
    - Added functionality to prompt users for their desired operations (e.g., resizing and/or changing EXIF data) and gather necessary inputs.
- **Image Processing Pipeline:**
    - The program now traverses a folder, opens images, applies modifications, and saves the processed files to the specified output location.
- **EXIF Handling:**
    - If EXIF changes are not desired, the program offers an option to copy the original EXIF data while adjusting key fields (e.g., image dimensions).
- **No Safety Checks Yet:**
    - Input validation (e.g., verifying folder existence, ensuring numeric input for percentages) is not yet implemented.
- **Foundation for Future Features:**
    - The groundwork allows for seamless addition of new image processing functions, leveraging the main class and TUI structure.

### Version 0.0.1: Initial Setup
- **Foundation Work:**
    - Established the groundwork for the project, focusing on testing and selecting the most effective tools. Transitioned from PyExifTool and Wand to Pillow and Piexif to minimize dependencies and streamline usability.
- **Proof of Concept:**
    - Conducted extensive testing and developed proof-of-concept functions to evaluate how various libraries integrate and perform.
- **TUI Development:**
    - Opted to use simple_term_menu instead of textual for the terminal-based user interface (TUI), leveraging prior experience to accelerate functional development over interface design.
- **AI Exploration:**
    - Tested local generative AI tools such as OpenCoder and Qwen2-Coder, exploring their potential for future project integration.
- **Project Status:**
    - The majority of work so far focuses on proof-of-concept implementation and experimentation.
