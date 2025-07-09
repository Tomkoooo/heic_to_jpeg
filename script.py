import os
import sys
from pathlib import Path
from PIL import Image
import pillow_heif

def get_script_dir():
    """Az EXE futtatási mappáját adja vissza, ha csomagolva van."""
    if getattr(sys, 'frozen', False):
        # Ha PyInstaller-rel csomagolva van
        return os.path.dirname(sys.executable)
    else:
        # Ha sima Python szkriptként fut
        return os.path.dirname(os.path.abspath(__file__))

def convert_heic_to_jpg(heic_path):
    try:
        # Ellenőrizzük, hogy a fájl létezik-e és HEIC kiterjesztésű-e
        if not os.path.exists(heic_path) or not heic_path.lower().endswith(('.heic', '.heif')):
            print(f"Hiba: '{heic_path}' nem létezik vagy nem HEIC fájl.")
            return None

        # Kimeneti mappa: a szkript/EXE mappája mellett egy 'Converted' mappa
        output_dir = os.path.join(get_script_dir(), "Converted")
        os.makedirs(output_dir, exist_ok=True)

        # JPG fájl neve generálása
        base_name = os.path.splitext(os.path.basename(heic_path))[0]
        jpg_path = os.path.join(output_dir, f"{base_name}.jpg")

        # HEIC fájl beolvasása
        heic_image = pillow_heif.read_heif(heic_path)
        image = Image.frombytes(
            heic_image.mode,
            heic_image.size,
            heic_image.data,
            "raw",
            heic_image.mode,
            heic_image.stride,
        )

        # JPG formátumba konvertálás és mentés
        image.save(jpg_path, "JPEG", quality=95)
        print(f"Sikeres konverzió: {jpg_path}")
        return jpg_path

    except Exception as e:
        print(f"Hiba a konverzió során: {e}")
        return None

def open_image(jpg_path):
    try:
        # JPG fájl megnyitása a Windows alapértelmezett képnézegetőjével
        os.startfile(jpg_path)
    except Exception as e:
        print(f"Hiba a kép megnyitása során: {e}")

def main():
    if len(sys.argv) < 2:
        print("Használat: heic_to_jpg.exe <heic_fájl_útvonala>")
        sys.exit(1)

    heic_path = sys.argv[1]
    jpg_path = convert_heic_to_jpg(heic_path)
    if jpg_path:
        open_image(jpg_path)

if __name__ == "__main__":
    main()