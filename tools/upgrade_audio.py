import urllib.request
import zipfile
import io
import os
import shutil

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

def download_and_extract_sound(zip_url, file_mapping):
    print(f"Downloading {zip_url}...")
    req = urllib.request.Request(zip_url, headers={'User-Agent': 'Mozilla/5.0'})
    r = urllib.request.urlopen(req).read()
    z = zipfile.ZipFile(io.BytesIO(r))
    
    for zip_path, target_name in file_mapping.items():
        print(f"Extracting {zip_path} to {target_name}...")
        try:
            source = z.open(zip_path)
            target_path = os.path.join(ASSETS_DIR, target_name)
            with open(target_path, "wb") as f:
                shutil.copyfileobj(source, f)
        except KeyError:
            print(f"Warning: {zip_path} not found in zip.")

def main():
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)

    # 1. Kenney Interface Sounds
    interface_url = 'https://kenney.nl/media/pages/assets/interface-sounds/d23a84242e-1677589452/kenney_interface-sounds.zip'
    interface_mapping = {
        'Audio/click_001.ogg': 'click.ogg',
        'Audio/click_002.ogg': 'select.ogg',
        'Audio/confirmation_001.ogg': 'confirm.ogg',
        'Audio/error_001.ogg': 'error.ogg',
        'Audio/drop_002.ogg': 'bump.ogg',
        'Audio/question_001.ogg': 'warn.ogg',
        'Audio/confirmation_002.ogg': 'success.ogg',
        'Audio/tick_001.ogg': 'typing.ogg',
        'Audio/maximize_008.ogg': 'blip.ogg',
        'Audio/scroll_001.ogg': 'drumroll.ogg' # Placeholder for drumroll
    }
    download_and_extract_sound(interface_url, interface_mapping)

    # 2. Kenney Casino Audio
    casino_url = 'https://kenney.nl/media/pages/assets/casino-audio/f578a13f51-1721639069/kenney_casino-audio.zip'
    casino_mapping = {
        'Audio/chips-handle-3.ogg': 'cash.ogg',
        'Audio/chip-lay-1.ogg': 'buy.ogg'
    }
    download_and_extract_sound(casino_url, casino_mapping)
    
    # 3. Clean up old extensions where needed
    # (The game audio module usually relies on the filename, but audio.py plays whatever is passed, 
    # except we need to make sure the extensions match what's in the code, or update the code to try .ogg)

if __name__ == "__main__":
    main()
