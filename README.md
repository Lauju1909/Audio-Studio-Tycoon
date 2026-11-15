# Audio Studio Tycoon v4.3.0 — Native Rust Edition

> [!IMPORTANT]
> **100% Screenreader-optimiert & Nativ in Rust (64-Bit)!**
> Dieses Spiel wurde komplett in **Rust** entwickelt, um maximale Geschwindigkeit (Simulation & Start in wenigen Millisekunden), hohe Stabilität und eine durchgängig logische Spielmechanik von **1930 bis in die Zukunft (2035+)** zu bieten. Es nutzt direktes 64-Bit-FFI für **Prism (`prism.dll`)** und **Tolk (`Tolk.dll`)** (NVDA, JAWS, Windows OneCore, SAPI, Braille) sowie native Win32/WinMM-Audioausgabe. Die Benutzeroberfläche und Sprachausgabe lassen sich jederzeit per `F8` oder `Strg+L` nahtlos zwischen **Deutsch** und **Englisch** umschalten.

---

## Was ist neu & welche Tycoon-Mechaniken stecken in Version 4.3.0?

### 1. Native 64-Bit Rust Engine & Barrierefreiheit
- Sofortiger Programmstart ohne Python- oder Pygame-Overhead.
- Native Win32-Oberfläche (`user32.dll` / `gdi32.dll`, Double-Buffered High-Contrast Dark UI) und verzögerungsfreie WAV/MP3-Effekte über `winmm.dll`.
- Dedizierter Hintergrund-Thread für `prism.dll` und `Tolk.dll` verhindert jegliches Ruckeln bei der Sprachausgabe und fährt beim Beenden sauber herunter (`stop -> free -> shutdown`).
- Akustischer Grenz-Bump am Anfang und Ende jeder Liste, Sprach-Wiederholung/Statusabfragen (`F`, `S`, `H`) sowie persistente Speicherslots (`save_slot_*.json`) und Einstellungen (`settings.json`).

### 2. Historisch stimmige Zeitlinie (1930–2035+, 7 Ären, 51 Plattformen & 97 Jahresereignisse, 48 Wochen/Jahr)
- **1930–1949 — Goldene Radio- & Schellack-Ära:** u. a. `Radio-Sendernetz (AM)`, `Schellack-Schallplatte (78 RPM)`, `Hand-Abakus`, `Mechanischer Spielautomat`, `Zuse Z1`, `Zuse Z3 (Relais-Rechner)`, `ENIAC Röhrenrechner`.
- **1950–1969 — Magnetband-, Stereo- & Mainframe-Ära:** u. a. `Vinyl-LP (33 RPM)`, `UNIVAC I Mainframe`, `Nimrod`, `EDSAC (OXO)`, `UKW-Transistorradio (FM)`, `PDP-1 (Spacewar-System)`, `Kompaktkassette (MC Stereo)`, `IBM System/360`.
- **1970–1979 — Arcade- & Analog-Synthesizer-Ära:** u. a. `Arcade-Automat (Münzspiel)`, `Magnavox Odyssey`, `Fairchild Channel F`, `Atari 2600 (VCS)`, `Apple II`, `Commodore PET`.
- **1980–1989 — 8-Bit Heimcomputer, FM-Synthese & CD-Ära:** u. a. `PC (MS-DOS / Soundkarte)`, `Commodore 64 (SID 6581)`, `ZX Spectrum`, `Vectrex`, `Famicom (NES)`, `Commodore Amiga (Paula)`, `Atari ST (YM2149 MIDI)`, `Sega Genesis (Mega Drive)`, `Game Boy`.
- **1990–1999 — 16/32-Bit Multimedia & 3D-Audio-Ära:** u. a. `SNES (Super Nintendo)`, `Neo Geo (YM2610)`, `PlayStation 1`, `Sega Saturn`, `Nintendo 64`, `Dreamcast`.
- **2000–2014 — Online-, Digitalvertrieb- & HD-Audio-Ära:** u. a. `PlayStation 2`, `PC (Digital / Steam)`, `Game Boy Advance`, `Nintendo DS`, `Xbox 360`, `PlayStation 3`, `Smartphone (iOS / Android)`, `PlayStation 4`.
- **2015–2035+ — Spatial Audio, VR, KI & Neural-Ära:** u. a. `VR-Headset (Spatial Audio)`, `Switch`, `Cloud-Console`, `PlayStation 5`, `Meta Quest 2 (VR)`, `Steam Deck`, `Neural-Box 1 (BCI Audio)`.
- **97 individuelle historische Jahresereignisse (`1930–2026` + Endlosmodus):** Jedes Jahr bietet eigene Ereignisse, dynamische **Markttrends** (Trend-Thema & Trend-Genre), Plattform-Freischaltungen/Ruhestände, automatischen Entwurfs-Wechsel bei eingestellten Plattformen sowie einen `0,55x` Retro-Nischen-Marktfaktor für bereits eingestellte Plattformen.
- **Zeitstrahl & Epochen-Chronik (`1930–2026`):** Übersicht in der Charts-/GOTY-Ansicht über aktuelle Ära, aktive Plattformen, freigeschaltete Meilensteine (`1975`, `1985`, `1995`, `2026`) und die jüngsten Chronik-Einträge.

### 3. Tiefgehende Spielentwicklungs- & Publisher-Mechaniken
- **Themen-, Genre- & Sub-Genre-Kompatibilität (29 Themen, 11 Genres, 8 Sub-Genres):**
  - 8 Startthemen (+ 21 erforschbare) und 4 Startgenres (+ 7 erforschbare) mit handgeprüfter Synergie-Matrix (`0` bis `3` Sterne), die direkt in der Auswahl angezeigt wird.
  - **8 Sub-Genres** (*Klassisch*, *Story-Fokus*, *Rhythmus & Musik*, *Taktik & Runden*, *Wirtschaft & Aufbau*, *Arcade & Tempo*, *Survival & Atmosphäre*, *Open World & Sandbox*) mit eigener `1–3` Sterne-Synergie (`★★★ [3/3]` gibt `+3%` Qualität, `★☆☆ [1/3]` gibt `-3%`).
- **Zielgruppen-Kompatibilität (`Jeder`, `Jugendliche`, `Hardcore-Gamer`):**
  - Jede Kombination aus Thema, Genre und Zielgruppe besitzt eine eigene Passungsstufe (`3/3 Perfekt` mit `+0,04` Qualitätsbonus & `1,20x` Verkaufsfaktor, `2/3 Passend` neutral, `1/3 Unpassend` mit `-0,07` Abzug & `0,65x` Verkaufsfaktor).
- **Transparente 6-Slider-Profile & Empfehlungsfunktion:**
  - Jedes Genre hat ein klares Idealprofil über die 6 Studio-Slider (*Gameplay, Grafik, Sound, Story, KI, Welt*; Summe = `30` Punkte, max. `10` pro Slider). Im Entwicklungsmenü lässt sich das empfohlene Genre-Profil direkt laden oder manuell verfeinern.
- **Fortsetzungen, Franchise-System & Klassiker-Remasters:**
  - Bestehende Titel können als Fortsetzung entwickelt werden (inkl. automatischer Nummerierung bei leerem Titel). Eine **neue eigene Custom-Audio-Engine** (höheres `tech_level`) bringt `+6%` Qualitätsbonus (`+0,06`), `+20` Hype und `1,25x` Verkaufsfaktor — das Wiederverwenden derselben oder einer älteren Engine führt dagegen zu `-4%` Franchise-Ermüdung.
  - **Klassiker-Remasters:** Eigene Titel ab `3` Jahren nach Erstveröffentlichung (sofern noch kein Remaster existiert) lassen sich für `50%` der Entwicklungskosten und `60%` der Entwicklungszeit auf der besten aktiven Plattform oder eigenen Konsole neu auflegen (`+4%` Qualität, `+15` Hype).
- **Vertrieb: Eigenvertrieb vs. Publisher-Verträge (5 Optionen):**
  - **Eigenvertrieb:** `0 €` Vorschuss, `0%` Umsatzabzug, `1,0x` Reichweite.
  - **4 Publisher** (*ÄtherWelle Verlag*, *Polyphonie Records*, *Global Sonic Interactive*, *OmniMedia Imperial*): gewähren einen direkten Cash-Vorschuss (`+8.000 €` bis `+150.000 €`) sowie höhere Marktreichweite (`1,25x` bis `2,15x`) gegen Umsatzbeteiligung (`25%` bis `40%`) und ein Review-Mindestziel (`5,5` bis `8,5`). Wird das Ziel erreicht, gibt es `+300` Fans & `+15` Hype; bei Verfehlen sinkt der Hype um `8`.
- **Kreative Studio-Entscheidungen während der Produktion *(1× pro Projekt)*:**
  - *Live-Foley- & Akustik-Session* (`3.000 €`): `+6%` Qualität, `+12` Hype.
  - *Signal- & Code-Refactoring* (`0 €`): entfernt alle aktuellen Bugs, `+4%` Qualität, `+1` Woche Entwicklungszeit.
  - *Community-Playtest* (`2.000 €`): `+5%` Qualität, `+250` Fans, `+15` Hype.
- **Vor-Release QA-Feinschliff & Mastering:**
  - Bis zu `3` Durchläufe für je `1.500 €`: behebt bis zu `4` Bugs und gewährt jeweils `+3%` Qualitätsbonus (`+0,03`).
- **Post-Mortem Spielbericht & Post-Release-Support:**
  - **Post-Mortem Analyse** *(1× pro veröffentlichtem Spiel)*: analysiert Thema-Genre-Synergie, Zielgruppen-Passung und die größte Slider-Abweichung vom Genre-Ideal, sendet eine Auswertungs-E-Mail und belohnt mit `+200` Fans, `+15` Hype sowie `+15` Studio-Know-How.
  - **Patches (`2.000 €`)** bereinigen verbliebene Bugs und frischen die aktiven Verkaufswochen auf; bis zu **2 DLCs pro Titel** (je `6.000 €`) verlängern den Lebenszyklus.

### 4. Studio-Ausbau, Auftragsarbeiten, Personal & Year-Gating
- **4 Schwierigkeitsgrade** (Startkapital `25.000 €` bis `150.000 €`) und **5 Studio-Ausbaustufen** (Platz für `2`, `4`, `8`, `14` oder `24` Mitarbeiter) plus Studio-Perks (z. B. Mischpult, Foley-Studio).
- **Auftragsarbeiten:** 4 ära-skalierte Vertragstypen für sichere Einnahmen bei pünktlichem Abschluss (oder Vertragsstrafe bei Fristüberschreitung).
- **Personal, Fortbildung & Erholungsurlaub:**
  - Fortbildungen (`5.000 €`, `2` Wochen) steigern alle Skills um `+6` und das Mitarbeiter-Level um `+1` (während Urlaub nicht startbar).
  - Erholungsurlaub (`1.000 €`, `3` Wochen) regeneriert Moral & Ausdauer; beurlaubte oder fortgebildete Mitarbeiter werden aktiv aus `active_employees()` gefiltert.
- **21 Engine-Features (1930–2026), 10 Forschungstechnologien (1930–2022) & Eigene Engine-Lizenzierung:** Selbst entwickelte Custom-Audio-Engines (ab Index 1; die Starter-Engine `Basis-Tonstudio V1` ist nicht lizenzierbar) können im Forschungsmenü an Drittstudios lizenziert werden und bringen wöchentliche Royalties (`Tech-Level * 350 €`/Woche).
- **Best Audio Design Award („Goldenes Mikrofon“):** Zum Jahreswechsel erhalten Spiele des Vorjahres mit hohem Sound-Fokus (`Sound >= 7`) und starker Wertung (`>= 7,5`) die Auszeichnung „Goldenes Mikrofon“ (`+15.000 €`, `+400` Fans, `+15` Hype).
- **Konkurrenz-Übernahmen & Tochterstudio-Dividenden:** Übernommene Konkurrenzstudios im Bank-/Rivalenmenü schütten wöchentlich Tochterstudio-Dividenden (`max(Wert / 250, 400) €`/Woche) direkt in die Studiokasse und den Gesamtumsatz aus.
- **12 Studio-Erfolge & Meilensteine (1930–2026):** 12 Meilensteine über die gesamte Studiohistorie (vom ersten Release über *8.0+ Hit*, *Hardware-Pionier*, *Musiklabel-Mogul*, *SoundCon-Bühnenstar*, *Branchen-Konsolidierer*, *Goldenes Mikrofon* bis *Jahrhundert-Legende ab 2026*) inklusive Geld-, Fan- & Hype-Prämien sowie Übersicht in der Charts-/GOTY-Ansicht.
- **Strikte Jahres-Freischaltungen (Year-Gating):**
  - **Hardware-Labor (Eigene Soundkarten & Konsolen):** ab **1975** (oder mit entsprechender Forschung).
  - **Eigenes Soundtrack-Label:** ab **1985**.
  - **SoundCon Messe & AudioPass-Abo-Dienst:** ab **1995**.

---

## Steuerung & Hotkeys

| Taste | Funktion |
| :--- | :--- |
| **Pfeil Auf / Ab** | Navigation in Menüs und Listen (mit akustischem Grenz-Bump am Anfang/Ende) |
| **Pfeil Links / Rechts** | Werte anpassen (6 Studio-Slider, Lautstärke, Abo-Preis, Auswahlfelder) |
| **Enter** | Auswahl bestätigen / Aktion ausführen |
| **Backspace / Esc** | Zurück zum vorherigen Menü |
| **Leertaste / 0** | Spielzeit pausieren / fortsetzen |
| **1, 2, 3** | Spielgeschwindigkeit (`1x`, `2x`, Ultra `4x`) |
| **W** | Eine Woche manuell voranschreiten |
| **F** | **Finanz-Übersicht** (Kontostand, Gehälter, Miete, Kredit, Umsatz) sofort vorlesen |
| **S** | **Studio-Status** (Datum, Ära, Fans, Hype, Team, aktives Projekt, Trend) sofort vorlesen |
| **H** | Tastenbelegung & Hilfe vorlesen |
| **F8 / Strg+L** | **Sprache sofort umschalten** (`Deutsch <-> Englisch`) bei gleicher Cursor-Position |
| **Strg+Shift+D** | Entwickler-Modus ein-/ausschalten |
| **D** | Entwickler-Menü öffnen (wenn Entwickler-Modus aktiv ist) |

---

## Starten, Bauen & Testen

### Spiel starten
```bat
Audio_Studio_Tycoon.exe
```
oder über `run_game.bat` bzw. `cargo run --release`.

### Automatisierte Tests, Headless-Verifikation & Release-Build
```bat
cargo test
cargo build --release
Audio_Studio_Tycoon.exe --verify
```
oder einfach per Doppelklick auf `build_game.bat` (führt die **31 automatisierten Unit- & Integrationstests** per `cargo test`, `cargo build --release`, den Kopierschritt nach `Audio_Studio_Tycoon.exe` und `--verify` automatisch aus).
Für eine schnelle CLI-Prüfung unterstützt die Executable außerdem `--version` (`-V`) und `--headless-demo`.
