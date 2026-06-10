import sys
import re
import json
import urllib.request
import urllib.parse
import time

def translate(text, target_lang="de", source_lang="en"):
    try:
        placeholders = {}
        def replacer(match):
            ph = match.group(1)
            token = f"__PH_{len(placeholders)}__"
            placeholders[token] = ph
            return token
        protected_text = re.sub(r"\{([^}]+)\}", replacer, text)
        encoded_text = urllib.parse.quote(protected_text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={encoded_text}"
        
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode("utf-8"))
            translated = "".join([sentence[0] for sentence in result[0]])
            for token, ph in placeholders.items():
                token_pattern = re.compile(token.replace("_", r"_?\s*"))
                translated = token_pattern.sub(f"{{{ph}}}", translated)
            return translated
    except Exception as e:
        print(f"Error translating: {e}")
        return text

sys.path.append('.')
from translations import TRANSLATIONS

en = TRANSLATIONS.get("en", {})
de = TRANSLATIONS.get("de", {})

updates = {}
for k, v in en.items():
    if v == de.get(k) and len(v) > 10:
        if k not in ["Action-RPG", "Beat 'em Up", "Arcade Racing", "Point & Click", "Sandbox/Voxel", "Tower Defense", "Visual Novel", "Survival Horror", "Social Networking"]:
            print(f"Translating {k}...")
            translated = translate(v)
            updates[k] = translated
            time.sleep(0.5)

print(f"Translated {len(updates)} strings.")

with open("updates.json", "w", encoding="utf-8") as f:
    json.dump(updates, f, indent=2, ensure_ascii=False)
