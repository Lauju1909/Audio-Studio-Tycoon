import requests
import os
import sys

# Configuration
TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    print("Error: GITHUB_TOKEN environment variable not set.")
    sys.exit(1)
OWNER = "Lauju1909"
REPO = "Audio-Studio-Tycoon"
TAG = "v2.0.0"
FILE_PATH = r"c:\Users\lauri\.gemini\antigravity\scratch\game_dev_tycoon_2\Audio_Studio_Tycoon_v2.0.zip"
FILE_NAME = "Audio_Studio_Tycoon_v2.0.zip"

def create_and_upload():
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 1. Create Release
    print(f"Creating release for tag {TAG}...")
    release_url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases"
    data = {
        "tag_name": TAG,
        "name": f"Release {TAG}",
        "body": "Stabiler Build 2.0: Installer Fix + Keyboard focus Grab für Screenreader.",
        "draft": False,
        "prerelease": False
    }
    
    response = requests.post(release_url, headers=headers, json=data)
    if response.status_code == 201:
        print("Release created successfully.")
        release_data = response.json()
    elif response.status_code == 422: # Already exists
        print("Release already exists. Fetching info...")
        tag_url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{TAG}"
        response = requests.get(tag_url, headers=headers)
        release_data = response.json()
    else:
        print(f"Error creating/fetching release: {response.status_code}")
        print(response.text)
        return

    upload_url = release_data['upload_url'].split('{')[0]
    
    # 2. Upload Asset
    print(f"Uploading {FILE_NAME}...")
    headers['Content-Type'] = 'application/zip'
    
    # Remove existing asset if it exists
    for asset in release_data.get('assets', []):
        if asset['name'] == FILE_NAME:
            print(f"Deleting existing asset {FILE_NAME}...")
            requests.delete(asset['url'], headers=headers)

    with open(FILE_PATH, 'rb') as f:
        params = {'name': FILE_NAME}
        upload_response = requests.post(upload_url, headers=headers, params=params, data=f)

    if upload_response.status_code == 201:
        print("Upload successful!")
        print(f"Release URL: {release_data['html_url']}")
    else:
        print(f"Upload failed: {upload_response.status_code}")
        print(upload_response.text)

if __name__ == "__main__":
    create_and_upload()
