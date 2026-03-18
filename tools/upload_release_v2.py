import os
import requests
import sys

# Configuration
TOKEN = os.getenv("GITHUB_TOKEN") 
if not TOKEN:
    print("Error: GITHUB_TOKEN environment variable not set.")
    sys.exit(1)

OWNER = "Lauju1909"
REPO = "Audio-Studio-Tycoon"
TAG = "v2.2.1"
NAME = "Audio Studio Tycoon v2.2.1 (Patch)"
BODY = "Release 2.2.1 - Historisches Bugfix Release\n\nFixes:\n- UnboundLocalError bei Jahreswechsel behoben.\n- Rivalen-Score skaliert jetzt korrekt ab 1930.\n- GOTY-Auswahl filtert jetzt präzise nach historischem Jahr.\n\nFeatures (aus v2.2.0):\n- Vollständige historische Plattformen (1930-2026).\n- 50+ historische Engine-Features mit Beschreibungen.\n- 35+ historische Jahresevents mit Marktauswirkungen."

FILE_PATH = r"c:\Users\lauri\.gemini\antigravity\scratch\game_dev_tycoon_2\Audio_Studio_Tycoon_v2.2.1.zip"
FILE_NAME = "Audio_Studio_Tycoon_v2.2.1.zip"

def upload_asset():
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    print(f"Checking if release {TAG} exists...")
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{TAG}"
    response = requests.get(url, headers=headers)
    
    release_data = None
    if response.status_code == 200:
        release_data = response.json()
        print(f"Release {TAG} already exists.")
    else:
        print(f"Release {TAG} not found. Creating it...")
        create_url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases"
        data = {
            "tag_name": TAG,
            "name": NAME,
            "body": BODY,
            "draft": False,
            "prerelease": False
        }
        create_resp = requests.post(create_url, headers=headers, json=data)
        if create_resp.status_code != 201:
            print(f"Error creating release: {create_resp.status_code}")
            print(create_resp.text)
            sys.exit(1)
        release_data = create_resp.json()
        print("Release created successfully.")

    release_id = release_data['id']
    upload_url_base = release_data['upload_url'].split('{')[0]
    print(f"Release ID is: {release_id}")

    # Check if asset already exists and delete it if so
    for asset in release_data.get('assets', []):
        if asset['name'] == FILE_NAME:
            print(f"Asset {FILE_NAME} already exists. Deleting ID {asset['id']}...")
            delete_url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/assets/{asset['id']}"
            del_resp = requests.delete(delete_url, headers=headers)
            if del_resp.status_code == 204:
                print("Deleted existing asset.")
            else:
                print(f"Failed to delete asset: {del_resp.status_code}")

    # Upload the asset
    print(f"Uploading {FILE_NAME}...")
    
    # Needs to be a binary upload
    upload_headers = headers.copy()
    upload_headers['Content-Type'] = 'application/zip'
    
    if not os.path.exists(FILE_PATH):
        print(f"Error: Could not find {FILE_PATH} to upload.")
        sys.exit(1)
        
    with open(FILE_PATH, 'rb') as f:
        params = {'name': FILE_NAME}
        upload_response = requests.post(upload_url_base, headers=upload_headers, params=params, data=f)

    if upload_response.status_code == 201:
        print("Upload successful!")
        print("Asset URL:", upload_response.json().get("browser_download_url"))
    else:
        print(f"Upload failed: {upload_response.status_code}")
        print(upload_response.text)

if __name__ == "__main__":
    upload_asset()
