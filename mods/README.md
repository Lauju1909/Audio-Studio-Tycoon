# 📦 Mods für Audio Studio Tycoon

Willkommen im Mod-Ordner! Hier kannst du eigene Mods für das Spiel erstellen.

## So funktioniert das Mod-System

Das Spiel scannt beim Start diesen Ordner automatisch nach Mods.
Jede Mod ist ein **Unterordner** mit einer `mod.json`-Datei darin.

Die Mods werden im Spiel unter **"Lokaler Mod-Manager"** (erreichbar aus dem Hauptmenü) verwaltet.
Dort kannst du jede Mod mit der **Enter-Taste** aktivieren oder deaktivieren.

---

## 📁 Struktur einer Mod

```
mods/
└── meine_mod/           <-- Name des Subordners (beliebig)
    └── mod.json         <-- Pflicht-Datei
```

---

## 📄 Aufbau der mod.json

```json
{
  "id": "meine_mod_01",
  "name": "Mein toller Mod",
  "author": "Dein Name",
  "version": "1.0",
  "description": "Beschreibung was diese Mod macht.",

  "add_topics": [
    {
      "name": "Wikinger",
      "trend_text": "Wikinger-Spiele sind gerade mega angesagt!"
    },
    {
      "name": "Raumstation"
    }
  ],

  "add_genres": [
    {
      "name": "Survival-Sandbox",
      "trend_text": "Survival-Sandbox boomt in den Charts!"
    }
  ]
}
```

### Erklärung der Felder:

| Feld | Pflicht | Beschreibung |
|---|---|---|
| `id` | ✅ Ja | Eindeutige ID (keine Leerzeichen, keine Sonderzeichen) |
| `name` | ✅ Ja | Anzeigename im Spiel |
| `author` | ✅ Ja | Dein Name |
| `version` | ✅ Ja | Versionsnummer als Text (z.B. `"1.0"`) |
| `description` | Nein | Kurze Beschreibung |
| `add_topics` | Nein | Liste neuer Spielthemen |
| `add_genres` | Nein | Liste neuer Spielgenres |
| `trend_text` | Nein | Nachricht im Markttrend-System |

---

## ✅ Schritt-für-Schritt Anleitung

1. **Ordner erstellen**: Erstelle einen neuen Ordner in `mods/`, z.B. `mods/mein_supermod/`
2. **mod.json erstellen**: Öffne einen Texteditor (Notepad, VSCode etc.) und erstelle die Datei `mod.json` im neuen Ordner
3. **Inhalt einfügen**: Füge JSON-Inhalt nach dem obigen Muster ein, speichere die Datei als UTF-8
4. **Spiel starten**: Beim nächsten Spielstart liest das Spiel deinen Mod automatisch ein
5. **Mod aktivieren**: Im Spiel → Hauptmenü → "Lokaler Mod-Manager" → deinen Mod wählen → Enter drücken
6. **Spielen**: Neue Themen und Genres erscheinen jetzt bei der Spielentwicklung!

---

## ⚠️ Hinweise

- Die `id` muss eindeutig sein! Zwei Mods mit gleicher ID führen zu Problemen.
- Nur **UTF-8** Kodierung für die `mod.json` nutzen.
- Mods werden beim **nächsten Neustart** aktiv (nach Aktivierung im Mod-Manager).
- Den `test_mod` Ordner kannst du als Vorlage nutzen.

---

*Viel Spaß beim Modden! 🎮*
