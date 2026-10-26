"""Verlinkt Menue-Untermodule: Klassen verweisen einander ueber Modul-Globals.

Nach dem Aufteilen einer Menue-Datei in mehrere Module sehen alle Untermodule die
oeffentlichen Klassen der Geschwister-Module (spaetere Module gewinnen bei Duplikaten,
wie vorher in der einzelnen Datei).
"""


def link_namespaces(modules):
    exported = {}
    for mod in modules:
        for key, value in vars(mod).items():
            if isinstance(value, type) and value.__module__ == mod.__name__:
                exported[key] = value
    for mod in modules:
        for key, value in exported.items():
            # Eigene Klassen nicht ueberschreiben: lokale Definition bleibt gueltig.
            if key not in vars(mod):
                setattr(mod, key, value)
