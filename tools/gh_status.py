import urllib.request, json
try:
    req = urllib.request.Request('https://api.github.com/repos/Lauju1909/Audio-Studio-Tycoon/releases')
    with urllib.request.urlopen(req) as response:
        releases = json.loads(response.read().decode('utf-8'))
        for r in releases[:2]:
            print(f"ID: {r.get('id')}")
            print(f"Tag: {r.get('tag_name')}")
            print(f"Pre: {r.get('prerelease')}")
            print(f"Draft: {r.get('draft')}")
            print("---")
except Exception as e:
    print(str(e))
