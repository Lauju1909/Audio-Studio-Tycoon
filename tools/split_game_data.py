"""Zerlegt game_data.py verbatim in das data/-Paket (Fassade bleibt).

Nicht-Funktionen landen je nach Zeilenbereich in einem Themenmodul (Reihenfolge der
Originaldatei bleibt erhalten, spaetere Duplikate ueberschreiben wie vorher).
Funktionen kommen nach data/helpers.py und sehen alle Konstanten.
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "game_data.py"
text = SRC.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
lines = text.split("\n")
tree = ast.parse(text)

MODULES = [  # (name, first line, doc)
    ("core", 1, "Grundkonstanten (Jahre, Sprachen)."),
    ("content", 30, "Themen, Genres, Plattformen, Zielgruppen, Technologien, Engine-Features."),
    ("people", 705, "Mitarbeiter, Rollen, Traits und Entwicklungs-Events."),
    ("studio", 951, "Buero, Bauobjekte, Spielgroessen, Marketing, Training."),
    ("economy", 1193, "Trends, Publisher, Mail- und Review-Templates."),
    ("events", 1369, "Zufalls-, historische und Jahres-Events."),
    ("meta", 1843, "Erfolge, Merch, Esports, Upgrades, Hardware, Fanpost, Persoenlichkeit."),
]

chunks = {m[0]: [] for m in MODULES}
helpers = []
prev_end = 0
for n in tree.body:
    seg = lines[prev_end:n.end_lineno]
    prev_end = n.end_lineno
    if isinstance(n, ast.FunctionDef):
        helpers.append("\n".join(seg))
        continue
    mod = [m for m in MODULES if m[1] <= n.lineno][-1][0]
    chunks[mod].append("\n".join(seg))

data = ROOT / "data"
data.mkdir(exist_ok=True)
prior = []
for name, _, doc in MODULES:
    body = "\n".join(chunks[name]).strip("\n")
    if name == "core":  # Docstring des Originals beibehalten
        head = ""
    else:
        head = f'"""{doc}"""\n' + "".join(f"from data.{p} import *  # noqa: F401,F403\n" for p in prior) + "\n"
    (data / f"{name}.py").write_text(head + body + "\n", encoding="utf-8", newline="\n")
    prior.append(name)
hp = '"""Zugriffsfunktionen auf die Spieldaten."""\n' + "".join(
    f"from data.{p} import *  # noqa: F401,F403\n" for p in prior) + "\n\n" + "\n\n".join(h.strip("\n") for h in helpers) + "\n"
(data / "helpers.py").write_text(hp, encoding="utf-8", newline="\n")
(data / "__init__.py").write_text('"""Spieldaten-Paket (Inhalte getrennt von Logik)."""\n', encoding="utf-8", newline="\n")
facade = '"""Fassade: alle Spieldaten liegen im Paket data/ (siehe data/*.py)."""\n' + "".join(
    f"from data.{p} import *  # noqa: F401,F403\n" for p in prior + ["helpers"])
SRC.write_text(facade, encoding="utf-8", newline="\n")
print("ok")
