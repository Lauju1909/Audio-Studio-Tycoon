import urllib.request
import re
import os
import sys

# Pretend to be a browser to avoid 406 Not Acceptable
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def download_ui_sounds():
    url = "https://soundimage.org/sfx-ui/"
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    print(f"Fetching {url}...")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching page: {e}")
        return

    # Find .mp3 links
    mp3_links = re.findall(r'href=[\'"]([^\'"]+\.mp3)[\'"]', html)
    
    # Filter for UI sounds, pick a few specific ones or just the first 4
    ui_sounds = [link for link in mp3_links if "UI" in link or "Click" in link or "Select" in link or "Menu" in link]
    if not ui_sounds:
        ui_sounds = mp3_links[:4] # fallback

    downloads = [
        ("select.mp3", ui_sounds[0] if len(ui_sounds) > 0 else None),
        ("confirm.mp3", ui_sounds[1] if len(ui_sounds) > 1 else None),
        ("bump.mp3", ui_sounds[2] if len(ui_sounds) > 2 else None),
        ("buy.mp3", ui_sounds[3] if len(ui_sounds) > 3 else None)
    ]

    for name, link in downloads:
        if not link:
            continue
        print(f"Downloading {link} to {name}...")
        try:
            req_dl = urllib.request.Request(link, headers=headers)
            with urllib.request.urlopen(req_dl) as dl_response:
                file_path = os.path.join(assets_dir, name)
                with open(file_path, 'wb') as f:
                    f.write(dl_response.read())
            print(f"Saved {name}")
        except Exception as e:
            print(f"Failed to download {link}: {e}")

if __name__ == "__main__":
    download_ui_sounds()
