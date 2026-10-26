import os
import re
import sys

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import setup_router
from audio import AudioManager
from logic import GameState

# Mock audio & state
audio = AudioManager()
state = GameState()
router = setup_router(audio, state)

registered_routes = set(router.dynamic_routes.keys())

menu_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "menus")
pattern = re.compile(r'(?:return\s+[\'"]([a-z0-9_]+)[\'"]|lambda\s*:\s*[\'"]([a-z0-9_]+)[\'"]|\'action\':\s*[\'"]([a-z0-9_]+)[\'"])')

all_found = set()

# Special non-route return strings or actions
ignored = {"quit", "error", "buy", "sell", "confirm", "cash", "fanfare", "bump", "click", "soundcon_menu", "soundcon_finish_confirm", "soundcon_result_menu", "soundcon_history_menu", "soundcon_qa"}

for root, _, files in os.walk(menu_dir):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fp:
                for line in fp:
                    for m in pattern.finditer(line):
                        r = m.group(1) or m.group(2) or m.group(3)
                        all_found.add((r, f))

missing = []
for r, filename in sorted(all_found):
    if r in ignored or r.startswith("soundcon_"):
        continue
    # Filter out obvious false positives like sounds or keywords
    if r in ["self", "none", "true", "false", "game_name", "genre", "topic", "audience", "platform"]:
        continue
    if not router.has_menu(r):
        missing.append((r, filename))

print(f"Total registered routes: {len(registered_routes)}")
print(f"Missing routes found in menus:")
for r, filename in missing:
    print(f"  {r} (in {filename})")
