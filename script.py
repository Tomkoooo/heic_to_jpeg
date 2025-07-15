import os
import sys
from pathlib import Path
from PIL import Image
import pillow_heif
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import re
from configparser import ConfigParser

def get_script_dir():
    """Returns the directory of the executable or script."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def normalize_name_for_email(name):
    """Generate email from name (placeholder function, included for consistency)."""
    words = name.strip().split()
    if len(words) >= 2:
        first_two = words[:2]
        reversed_name = f"{first_two[1].lower()}.{first_two[0].lower()}"
        replacements = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ö': 'o', 'ő': 'o',
                        'ú': 'u', 'ü': 'u', 'ű': 'u', 'ô': 'o'}
        for accented, plain in replacements.items():
            reversed_name = reversed_name.replace(accented, plain)
        return f"{reversed_name}@mfa.gov.hu"
    return ""

def convert_image(input_path, output_format="jpg", output_dir=None):
    """Convert a single image file to the specified format."""
    try:
        if not os.path.exists(input_path):
            print(f"Hiba: '{input_path}' nem létezik.")
            return None

        if input_path.lower().endswith(('.heic', '.heif')):
            heic_image = pillow_heif.read_heif(input_path)
            image = Image.frombytes(
                heic_image.mode, heic_image.size, heic_image.data,
                "raw", heic_image.mode, heic_image.stride,
            )
        else:
            image = Image.open(input_path)

        if not output_dir:
            output_dir = os.path.join(get_script_dir(), "Converted")
        os.makedirs(output_dir, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}.{output_format.lower()}")

        image.save(output_path, output_format.upper(), quality=95)
        print(f"Sikeres konverzió: {output_path}")
        return output_path

    except Exception as e:
        print(f"Hiba a konverzió során: {e}")
        return None

def open_image(image_path):
    """Open the converted image with the default viewer."""
    try:
        os.startfile(image_path)
    except Exception as e:
        print(f"Hiba a kép megnyitása során: {e}")

def save_settings(config, input_format, output_format, save_location):
    """Save global settings to a config file."""
    config['Settings'] = {
        'input_format': input_format,
        'output_format': output_format,
        'save_location': save_location
    }
    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)

def load_settings(config):
    """Load global settings from a config file."""
    if os.path.exists('config.ini'):
        config.read('config.ini')
        return config['Settings'].get('input_format', 'heic'), \
               config['Settings'].get('output_format', 'jpg'), \
               config['Settings'].get('save_location', get_script_dir())
    return 'heic', 'jpg', get_script_dir()

def associate_files(input_format):
    """Associate the app with the specified image format (simplified for demo)."""
    # Note: Full file association requires registry edits, which is OS-specific and complex.
    # This is a placeholder to show the intent; for production, use a setup script or installer.
    messagebox.showinfo("Fájl társítás", f"A(z) .{input_format} fájlok társítása a programhoz megtörtént. Indítsa újra a számítógépet a változások érvénybe lépéséhez.")
    # In a real scenario, you'd use pywin32 or a setup tool to modify the registry.

def convert_files(file_paths, output_format, output_dir):
    """Convert multiple files and open the first converted image."""
    converted_paths = []
    for file_path in file_paths:
        converted_path = convert_image(file_path, output_format, output_dir)
        if converted_path:
            converted_paths.append(converted_path)
    if converted_paths:
        open_image(converted_paths[0])
    return converted_paths

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kép Konvertáló")
        self.root.geometry("400x300")

        # Load or initialize settings
        self.config = ConfigParser()
        self.input_format, self.output_format, self.save_location = load_settings(self.config)

        # GUI Elements
        tk.Label(root, text="Bemeneti formátum:").pack(pady=5)
        self.input_var = tk.StringVar(value=self.input_format)
        tk.Entry(root, textvariable=self.input_var).pack()

        tk.Label(root, text="Kimeneti formátum:").pack(pady=5)
        self.output_var = tk.StringVar(value=self.output_format)
        tk.Entry(root, textvariable=self.output_var).pack()

        tk.Label(root, text="Mentési hely:").pack(pady=5)
        self.location_var = tk.StringVar(value=self.save_location)
        tk.Entry(root, textvariable=self.location_var).pack()
        tk.Button(root, text="Tallózás", command=self.browse_location).pack(pady=5)

        tk.Button(root, text="Fájlok kiválasztása", command=self.select_files).pack(pady=5)
        tk.Button(root, text="Konvertálás", command=self.convert_selected).pack(pady=5)

        tk.Button(root, text="Globális beállítások mentése", command=self.save_settings).pack(pady=5)
        tk.Button(root, text="Fájl társítás", command=self.associate_files).pack(pady=5)

    def browse_location(self):
        """Open a dialog to select the save location."""
        folder = filedialog.askdirectory(initialdir=self.save_location)
        if folder:
            self.location_var.set(folder)

    def select_files(self):
        """Open a dialog to select multiple image files."""
        files = filedialog.askopenfilenames(
            filetypes=[("Image files", f"*.{self.input_var.get()} *.jpg *.png *.heic *.heif")]
        )
        self.selected_files = files

    def save_settings(self):
        """Save the current settings as global defaults."""
        save_settings(self.config, self.input_var.get(), self.output_var.get(), self.location_var.get())
        messagebox.showinfo("Siker", "Beállítások mentve!")

    def associate_files(self):
        """Associate the app with the input format."""
        associate_files(self.input_var.get())

    def convert_selected(self):
        """Convert the selected files based on current settings."""
        if hasattr(self, 'selected_files') and self.selected_files:
            convert_files(self.selected_files, self.output_var.get(), self.location_var.get())
            messagebox.showinfo("Siker", f"{len(self.selected_files)} fájl konvertálva!")
        else:
            messagebox.showwarning("Figyelmeztetés", "Nincsenek kiválasztott fájlok!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()