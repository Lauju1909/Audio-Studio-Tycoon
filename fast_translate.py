import sys
import re
import json
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

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
        return text

sys.path.append('.')
from translations import TRANSLATIONS

en = TRANSLATIONS.get("en", {})
de = TRANSLATIONS.get("de", {})

missing = []
for k, v in en.items():
    if v == de.get(k) and len(v) > 10:
        if k not in ["Action-RPG", "Beat 'em Up", "Arcade Racing", "Point & Click", "Sandbox/Voxel", "Tower Defense", "Visual Novel", "Survival Horror", "Social Networking"]:
            missing.append((k, v))
for k, v in de.items():
    if not v:
        missing.append((k, en.get(k, k)))

print(f"Translating {len(missing)} strings...")

def do_trans(item):
    k, v = item
    return k, translate(v)

with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(do_trans, missing)

for k, trans in results:
    de[k] = trans

# Also add empty strings correctly
for k in en.keys():
    if k not in de:
        de[k] = en[k]

with open("translations_new.py", "w", encoding="utf-8") as f:
    f.write('"""\nTranslations for Audio Studio Tycoon.\nOnly German is stored, other languages are translated on-the-fly.\n"""\n')
    with open("translations.py", "r", encoding="utf-8") as orig:
        content = orig.read()
        f.write(content[:content.find("TRANSLATIONS = {")])
    
    f.write("TRANSLATIONS = {\n")
    f.write('    "en": {\n')
    for i, (k, v) in enumerate(en.items()):
        f.write(f'        "{k}": {json.dumps(v, ensure_ascii=False)}')
        if i < len(en) - 1:
            f.write(",\n")
        else:
            f.write("\n")
    f.write('    },\n')
    f.write('    "de": {\n')
    for i, (k, v) in enumerate(de.items()):
        f.write(f'        "{k}": {json.dumps(v, ensure_ascii=False)}')
        if i < len(de) - 1:
            f.write(",\n")
        else:
            f.write("\n")
    f.write('    }\n')
    f.write('}\n')

print("Wrote to translations_new.py")
