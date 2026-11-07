# Audio Studio Tycoon v4.3.0 — Native Rust Edition

> [!IMPORTANT]
> **100% Screenreader-optimiert & Nativ in Rust (64-Bit)!**
> Dieses Spiel wurde komplett in **Rust** neu entwickelt, um maximale Geschwindigkeit (Simulation & Start in wenigen Millisekunden), absolute Absturzsicherheit und eine von Grund auf durchdachte, logische Spielmechanik von **1930 bis in die Zukunft (2035+)** zu bieten. Es nutzt direktes 64-Bit FFI für **Prism (`prism.dll`)** und **Tolk (`Tolk.dll`)** (NVDA, JAWS, Windows OneCore, SAPI, Braille) sowie native Win32/WinMM-Audioausgabe.

---

## Was ist neu in Version 4.3.0 (Rust-Überarbeitung)?

1. **Komplette Portierung auf Rust (Zero-Dependency Native 64-Bit Engine):**
   - Sofortiger Programmstart ohne Python-/Pygame-Overhead.
   - Native Win32-Oberfläche (`user32.dll` / `gdi32.dll` Double-Buffered High-Contrast Dark UI) und verzögerungsfreie WAV/MP3-Effekte über `winmm.dll`.
   - Dedizierter Hintergrund-Thread für `prism.dll` und `Tolk.dll` verhindert jegliches Ruckeln bei der Sprachausgabe und beendet sich sauber (`stop -> free -> shutdown`).

2. **Überarbeitetes, 100% logisches Spieldesign ("Dass alles Sinn macht"):**
   - **Historisch stimmige Zeitlinie (7 Ären von 1930 bis 2035+):**
     - **1930–1949:** Goldene Radio- & Schellack-Ära (`Radio-Sendernetz (AM)`, `Schellack-Hörspielplatte (78 RPM)`, `Mechanischer Spielautomat`) — kein unlogischer Start mit MS-DOS im Jahr 1930 mehr!
     - **1950–1969:** Transistor-, Vinyl-LP- & Mainframe-Ära (`Vinyl-LP`, `Früher Großrechner`, `Tonband-Kassette`).
     - **1970–1982:** Frühe Arcade- & 8-Bit-Pionierzeit (`Arcade-Automat`, `Atari VCS`, `Commodore 64 (SID)`).
     - **1983–1993:** 16-Bit Heimcomputer, FM-Synthese & Konsolen-Boom (`PC (MS-DOS / AdLib)`, `Commodore Amiga`, `NES`, `Game Boy`, `SNES`, `Sega Mega Drive`).
     - **1994–2005:** CD-ROM, 3D-Audio & frühes Internet (`PC Windows CD-ROM`, `PlayStation`, `Nintendo 64`, `PlayStation 2`, `Xbox`).
     - **2006–2017:** HD-Gaming, Digitaler Vertrieb & Mobile (`PC Digital / Steam`, `Xbox 360`, `PlayStation 3/4`, `Smartphone`, `Nintendo Switch`).
     - **2018–2035+:** Spatial Audio, VR, Cloud & Neural-Gaming (`PlayStation 5 (Tempest 3D)`, `VR-Headset (Binaural)`, `Neural-Audio Interface`).
   - **Sinnvolle Themen-Genre-Kompatibilitätsmatrix:**
     - Alle 29 Themen und 11 Genres haben handgeprüfte, logische Synergien (0 bis 3 Sterne) statt Zufallszahlen.
     - Beispiele: *Fantasy + RPG = 3/3 (Perfekt)*, *Rennwagen + Rennspiel = 3/3 (Perfekt)*, *Schach + Strategie/Puzzle = 3/3 (Perfekt)*, *Radio-Drama + Abenteuer/Horror = 3/3 (Perfekt)*, *Cyberpunk + RPG/Action = 3/3 (Perfekt)*.
     - Im Genre-Auswahlmenü zeigt das Spiel die Synergie zum gewählten Thema direkt an!
   - **Transparente Slider-Profile & Empfehlungsfunktion:**
     - Jedes Genre hat ein klares, logisches Idealprofil über die 6 Studio-Slider (*Gameplay, Grafik/Kulisse, Sound & Musik, Story & Dialoge, KI & Spiellogik, Welt & Atmosphäre*, Summe = 30 Punkte).
     - Auf Wunsch kann im Slider-Menü das empfohlene Genre-Profil direkt per Tastendruck geladen oder feinjustiert werden.
   - **Strikte Jahres-Freischaltung (Year-Gating) aller Subsysteme:**
     - **Hardware-Labor (Eigene Soundkarten & Konsolen):** ab **1975** (oder mit Forschung *Hardware-Labor*).
     - **Eigenes Soundtrack-Label (OST-Alben & Live-Konzerte):** ab **1985**.
     - **SoundCon Messe & AudioPass-Abo-Dienst:** ab **1995**.
   - **Sinnvolles Personal-, Urlaubs- & Schulungssystem:**
     - Mitarbeiter im Erholungsurlaub oder in einer Fortbildung werden aktiv aus `active_employees()` herausgefiltert und kehren nach Ablauf erholt bzw. höherstufig zurück.

---

## Steuerung & Hotkeys

| Taste | Funktion |
| :--- | :--- |
| **Pfeil Auf / Ab** | Navigation in Menüs und Listen (mit akustischem Grenz-Bump am Anfang/Ende) |
| **Pfeil Links / Rechts** | Werte anpassen (6 Studio-Slider, Lautstärke, Abo-Preis) |
| **Enter** | Auswahl bestätigen |
| **Backspace / Esc** | Zurück zum vorherigen Menü |
| **Leertaste / 0** | Spielzeit pausieren / fortsetzen |
| **1, 2, 3** | Spielgeschwindigkeit (Normal, Schnell, Ultra) |
| **W** | Eine Woche manuell voranschreiten |
| **F** | **Finanz-Übersicht** (Kontostand, Gehälter, Miete, Kredit, Umsatz) sofort vorlesen |
| **S** | **Studio-Status** (Datum, Ära, Fans, Hype, Team, aktives Projekt, Trend) sofort vorlesen |
| **H / F1** | Tastenbelegung & Hilfe vorlesen |
| **F8 / Strg+L** | **Sprache sofort umschalten** (Deutsch <-> Englisch) bei gleicher Cursor-Position |
| **F9 / F10** | Entwickler-Modus umschalten / Entwickler-Menü öffnen |

---

## Starten, Bauen & Testen

### Spiel starten
```bat
Audio_Studio_Tycoon.exe
```
oder über `run_game.bat` bzw. `cargo run --release`.

### Automatisierte Tests & Release-Build ausführen
```bat
cargo test
cargo build --release
Audio_Studio_Tycoon.exe --verify
```
oder einfach per Doppelklick auf `build_game.bat`.
