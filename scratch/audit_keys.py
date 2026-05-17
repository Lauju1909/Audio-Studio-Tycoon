import os
import re

root_dir = r"c:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon"
translations_file = os.path.join(root_dir, "translations.py")

with open(translations_file, "r", encoding="utf-8") as f:
    trans_content = f.read()

# Find all keys in translations.py (keys are like "key": "value")
all_keys = set(re.findall(r'"([^"]+)":\s*"', trans_content))

# Search for key usage in all .py files
used_keys = set()
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".py"):
            with open(os.path.join(dirpath, filename), "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                for key in all_keys:
                    if f"'{key}'" in content or f'"{key}"' in content:
                        used_keys.add(key)

unused_keys = all_keys - used_keys
print(f"Total keys: {len(all_keys)}")
print(f"Used keys: {len(used_keys)}")
print(f"Unused keys: {len(unused_keys)}")

# Also find keys that are used but NOT in translations.py
missing_keys = set()
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".py"):
            if filename == "translations.py": continue
            with open(os.path.join(dirpath, filename), "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                # Find all get_text('key') or get_text("key")
                found = re.findall(r'get_text\([\'"]([^\'"]+)[\'"]', content)
                for key in found:
                    if key not in all_keys and not key.startswith("story_") and not key.startswith("event_"):
                        missing_keys.add(key)

print(f"Missing keys (used but not defined): {missing_keys}")
