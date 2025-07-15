Universal Image Converter and HEIC to JPG Converter
This repository contains two executable applications for image conversion on Windows:

Universal Image Converter (universal_image_converter.exe)
HEIC to JPG Converter (heic_to_jpg.exe)

Both tools are designed to simplify image format conversion, with distinct features and use cases.
Universal Image Converter (universal_image_converter.exe)
Overview
The Universal Image Converter is a graphical Windows application built to handle multiple image conversions with customizable options. It allows batch processing of images, supports various input and output formats, and provides flexibility in save locations.
Features

Batch Conversion: Convert multiple image files simultaneously.
Customizable Formats: Select input and output formats (e.g., HEIC, JPG, PNG) via a user interface.
Save Location: Choose a custom directory for converted files, with a default "Converted" folder created alongside the executable.
Global Settings: Save preferences (input format, output format, save location) for reuse.
File Association: Associate the app with image file types (e.g., HEIC, JPG) for automatic conversion based on saved settings (requires manual setup or installer for full integration).

Usage

Run universal_image_converter.exe.
Enter or select the input format (e.g., "heic"), output format (e.g., "jpg"), and save location.
Click "Fájlok kiválasztása" to select multiple image files.
Click "Konvertálás" to convert the files.
Optionally, save settings with "Globális beállítások mentése" or associate file types with "Fájl társítás" (note: full association may require additional setup).

Notes

Supports HEIC/HEIF and common formats like JPG and PNG, but does not include WebP support.
The app creates a "Converted" folder in the same directory as the executable if not specified otherwise.
For file association, manual registry edits or a setup script may be needed for production use.

HEIC to JPG Converter (heic_to_jpg.exe)
Overview
The HEIC to JPG Converter is a lightweight executable designed specifically for converting HEIC/HEIF files to JPG. It integrates with the Windows Photos app and saves converted files to a "Converted" folder.
Features

Single-Purpose Conversion: Converts HEIC/HEIF files to JPG format only.
File Association: Can be associated with HEIC files to open them directly in Windows Photos, triggering automatic conversion.
Automatic Save: Saves converted files to a "Converted" folder created in the same directory as the executable.

Usage

Associate heic_to_jpg.exe with .heic and .heif file types:
Right-click a HEIC file, select "Open with" > "Choose another app."
Browse to heic_to_jpg.exe, check "Always use this app," and click OK.


Double-click any HEIC file to open it in Windows Photos; the app will convert it to JPG and save it in the "Converted" folder.
Converted files are accessible in the "Converted" folder alongside the executable.

Notes

This tool is optimized for HEIC-to-JPG conversion and does not support other formats or batch customization.
Ensure the executable and "Converted" folder remain in the same directory for proper functionality.

Installation

Ensure Python is installed with pillow and pillow_heif libraries (if building from source).
Install dependencies: py -m pip install pillow pillow_heif
Note: tkinter is included with Python and does not require separate installation.


Download the pre-built universal_image_converter.exe and heic_to_jpg.exe from the releases section.
Place both executables in the desired directory (e.g., C:\Users\skoda\Desktop\programs\heic_to_jpeg).

Building from Source

Clone this repository.
Install required packages: py -m pip install pillow pillow_heif.
Use a tool like PyInstaller to create executables:
For universal_image_converter.py: pyinstaller --onefile universal_image_converter.py
For the original heic_to_jpg.py (if provided): Adjust and build similarly.


Locate the generated .exe files in the dist folder.

Contributing
Feel free to submit issues or pull requests for enhancements, such as adding WebP support to the Universal Image Converter or improving file association.
License
MIT License (or specify your preferred license).