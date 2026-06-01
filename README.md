# Audio Studio Tycoon (v3.11.0-beta.1) ðŸš€

> [!IMPORTANT]
> **100% Screenreader-optimiert!** Dieses Spiel wurde von Grund auf fÃ¼r blinde und sehbehinderte Spieler entwickelt. Es nutzt modernste TTS-Technologie (Tolk) fÃ¼r eine nahtlose Spielerfahrung.

## ðŸŒŸ Ãœber das Spiel
GrÃ¼nde dein eigenes Spielestudio in der Pionierzeit von 1930 und fÃ¼hre es durch die Jahrzehnte bis in die ferne Zukunft. Entwickle innovative Audio-Spiele, stelle Talente ein und manage dein Imperium.

## ðŸš€ Quick Start Guide (Erste Schritte)
1. **Neues Spiel**: WÃ¤hle "Neues Spiel entwickeln" im HauptmenÃ¼.
2. **Konzept**: WÃ¤hle ein passendes Paar aus Thema und Genre (z.B. *Fantasy* & *RPG*).
3. **Entwicklung**: Nutze die Pfeiltasten, um die 6 Slider (Gameplay, Grafik, Sound, Story, KI, Welt) anzupassen. Ein Action-Spiel braucht mehr Gameplay, ein RPG mehr Story!
4. **VerÃ¶ffentlichung**: Sobald die Entwicklung abgeschlossen ist, kannst du das Spiel verÃ¶ffentlichen und die Reviews der Presse abwarten.
5. **Wachstum**: Nutze deine Gewinne fÃ¼r neue Forschung (Genres, Themen) oder stelle Mitarbeiter ein, um grÃ¶ÃŸere Projekte (Mittel, GroÃŸ, AAA) zu stemmen.

## âŒ¨ï¸ Steuerung & Hotkeys
Das Spiel wird komplett Ã¼ber die Tastatur gesteuert:

| Taste | Funktion |
| :--- | :--- |
| **Pfeil Auf/Ab** | Navigation in MenÃ¼s und Listen |
| **Pfeil Links/Rechts** | Werte anpassen (Slider, LautstÃ¤rke) |
| **Enter** | Auswahl bestÃ¤tigen |
| **Backspace / Esc** | ZurÃ¼ck zum vorherigen MenÃ¼ |
| **S** | **Status-Ãœbersicht** (Forschungspunkte, Fans, Mitarbeiter) |
| **F** | **Finanz-Check** (Kontostand, Gewinnberichte) |

## ðŸš€ Neue Features (v3.10.0-beta.1)
- **Engine-Lizenzierung**: Du kannst deine selbst entwickelten Engines an andere Studios lizenzieren und wÃ¶chentliche Einnahmen generieren!
- **Spiele-Portierungen**: Portiere deine erfolgreichen Spiele auf neue Plattformen, um neue KÃ¤uferschichten zu erschlieÃŸen.
- **SoundCon (JÃ¤hrliche Spielemesse)**:
  - Anmeldung in Woche 2 jedes Kalenderjahres.
  - WÃ¤hle zwischen vier StandgrÃ¶ÃŸen (*Klein*, *Mittel*, *GroÃŸ* und *Keynote-BÃ¼hne*).
  - Halte interaktive Q&A-Runden auf der BÃ¼hne ab und beantworte Fan-Fragen.
  - Gewinne massiven Hype, neue Fans und Prestige-Punkte durch eine spektakulÃ¤re Show.
  - Komplette SoundCon-Historie zur Nachverfolgung vergangener Messeerfolge.
- **Soundtrack-Labels (Dein eigenes Musiklabel)**:
  - GrÃ¼nde dein eigenes Plattenlabel, um die Soundtracks deiner Spiele zu vermarkten.
  - Katalogisiere deine Spiele und erhalte wÃ¶chentlich passive Streaming-Tantiemen.
  - SchlieÃŸe exklusive Radio-VertrÃ¤ge fÃ¼r deine Top-Soundtracks ab, um wÃ¶chentlich Hype und zusÃ¤tzliche Einnahmen zu generieren.
- **Save/Load-Persistenz & AbwÃ¤rtskompatibilitÃ¤t**:
  - Volle Datensicherung aller SoundCon- und Soundtrack-Label-Daten.
  - 100% abwÃ¤rtskompatibel mit SpielstÃ¤nden aus Version 3.9.0 durch robuste Standardwert-Fallbacks.
- **ÃœbersetzungsparitÃ¤t & Barrierefreiheit**:
  - Alle neuen MenÃ¼s (SoundCon und Soundtrack-Label) sind vollstÃ¤ndig in Deutsch und Englisch Ã¼bersetzt (100% ParitÃ¤t).
  - Volle lineare Keyboard-Navigation und akustische Grenzen-Feedback (Bump-Sound) fÃ¼r blinde Spieler.
- **Interaktive, sprachgefÃ¼hrte Tutorials**: Einsteigerfreundliche, vollstÃ¤ndig blindengerechte EinfÃ¼hrungen fÃ¼r alle wichtigen Spielbereiche:
  - ðŸŽ¬ **Willkommen & Steuerung** (Grundlagen der Navigation)
  - ðŸ¢ **BÃ¼ro & Zeitverlauf** (Wie die Zeit vergeht und Hotkeys)
  - ðŸ’» **Spielentwicklung** (Themenwahl, Platformen, Slider)
  - ðŸ”¬ **Forschung** (Technologien, Genres, Engines)
  - ðŸ‘¥ **Personalmanagement (HR)** (Einstellen, Fortbilden, Moral)
  - ðŸ“¢ **Marketing & Hype** (Kampagnen planen)
  - ðŸ’° **Finanzen & Bank** (Kredite, Aktienmarkt)
  - ðŸŒ **Mehrspielermodus** (Lobbys beitreten/erstellen)
- **Automatisierte Test-Suite**: StÃ¤ndige QualitÃ¤tskontrolle durch Testskripte (`test_tutorials.py`, `test_event_hype_fix.py`, etc.) zur Validierung aller SprachschlÃ¼ssel, Eingabe-Simulationen, Event-Berechnungen und Savegame-Sicherheit.
- **Robustes, barrierefreies Update-System**:
  - Vollautomatischer Update-Prozess Ã¼ber GitHub-Releases (sowohl Stable- als auch Beta-KanÃ¤le).
  - SicherheitsprÃ¼fung via SHA-256 Checksummen-Validierung zum Schutz vor unvollstÃ¤ndigen Downloads.
  - Fehlerfreies Windows-CMD-Installationsskript: Erkennt versionierte Dateien (`Audio_Studio_Tycoon_v*.exe`) und bereinigt Ã¤ltere Exe-Dateien vollautomatisch vor der Installation, um Konflikte zu vermeiden.
  - Volles akustisches und barrierefreies Feedback: PrÃ¤zise Sprachausgabe und Fehlersounds bei eventuellen Update-Problemen, statt stummem ZurÃ¼ckkehren ins HauptmenÃ¼.
- **StabilitÃ¤ts- und Logik-Optimierungen (v3.10.0-beta.1)**:
  - Behebung eines kritischen `KeyError`-Absturzes bei Hype-Boost-Zufallsereignissen (wie `viral_post`).
  - Behebung eines Speicher-Leaks bei historischen Jahresereignissen, wodurch die Spielleistung gesteigert und Savegame-Dateien signifikant verkleinert wurden.
  - Entfernung von redundantem E-Mail-Spam bei historischen Ereignissen zum Jahreswechsel.
## ðŸš€ Das ultimative Audio- & Community-Update (v3.11.0-beta.1)
- **Auftragsarbeiten (Contract Work)**:
  - Generiere schnelles Geld durch das ErfÃ¼llen von externen AuftrÃ¤gen (Code, Grafik, Sound, Design).
  - Skaliert mit deinem Firmen-Prestige!
- **Eigene Soundkarten-Herstellung & Hardware-Labor**:
  - VerfÃ¼gbar ab dem Jahr 1980.
  - Erforsche zukunftsweisende Audio-Technologien wie *FM-Synthese*, *Wavetable* oder *3D-Binaural*.
  - Entwickle deine eigenen Soundkarten und lizenziere sie auf dem Weltmarkt.
  - Generiere wÃ¶chentlich wachsende, passive Tantiemen basierend auf deinem aktuellen Marktanteil (mit realistischem Decay).
- **Fan-Post & Community-Center**:
  - Empfange wÃ¶chentlich Briefe deiner Fans und reagiere interaktiv im Community-Center darauf.
  - Triff weise Entscheidungen in Brief-Antworten und sichere dir Hype-Boosts, Spenden oder neue Fans.
- **Barrierefreiheits-Labor**:
  - Investiere im Community-Center in Screenreader-Tests, Audio-Description-Studien und Community-Betas mit blinden Spielern.
  - Baue eine Barrierefreiheits-Reputation auf, die wÃ¶chentlich neue Fans bringt, Bugs aktiver Projekte reduziert und Reviews leicht verbessert.
  - Hohe Reputation schaltet neue Meilensteine frei und kann jÃ¤hrliche Barrierefreiheits-ZuschÃ¼sse auslÃ¶sen.
- **Mitarbeiter-PersÃ¶nlichkeiten & BÃ¼ro-Events**:
  - Jeder Mitarbeiter besitzt jetzt einen einzigartigen Charakterzug (*Perfektionist*, *Chaot*, *Showmaster*, *Workaholic* oder *Gelassen*) mit individuellen Boni und Nachteilen auf die SpielqualitÃ¤t, Moral oder Entwicklungszeit.
  - WÃ¶chentliche BÃ¼ro-Ereignisse zwingen dich dazu, barrierefreie Teamentscheidungen bei Konflikten oder Synergien zu treffen.
- **Marketing-Jingle-Generator mit akustischer Vorschau**:
  - Kombiniere Musikspuren, Sprecher-Stile und Soundeffekte, um Radio-Jingles zur Bewerbung deiner aktuellen Spiele zu produzieren.
  - **Akustische Vorschau (Sound-Previews)**: Beim Navigieren und Fokussieren der Spuren wird sofort ein prÃ¤gnantes Audio-Feedback Ã¼ber den Screenreader oder Pygame-Mixer abgespielt (z.B. Chiptune -> Retro-Blips, Kassenklingeln bei Cash, Laser-FX, etc.), um blinden Spielern eine intuitive Kompositions-Erfahrung zu bieten.
- **Savegame-AbwÃ¤rtskompatibilitÃ¤t**:
  - 100%ige AbwÃ¤rtskompatibilitÃ¤t alter SpielstÃ¤nde (aus v3.10.0 und Ã¤lter). Neue Strukturen wie Fanpost, Jingles und Soundkarten-Projekte werden beim Laden automatisch mit robusten Default-Werten initialisiert, ohne SpielstÃ¤nde unbrauchbar zu machen.
- **Automatisierte Test-Suite**: StÃ¤ndige QualitÃ¤tskontrolle durch Testskripte (`test_audio_expansion.py`, `test_tutorials.py`, etc.) zur Validierung aller SprachschlÃ¼ssel, Eingabe-Simulationen, Event-Berechnungen und Savegame-Sicherheit.

## ðŸŽ“ Interaktives Tutorial-System
Das Spiel bietet ein brandneues, interaktives Tutorial-System. Beim ersten Betreten eines Kernbereichs (Forschung, HR, Finanzen etc.) startet automatisch eine sprachgefÃ¼hrte EinfÃ¼hrung. Diese erklÃ¤rt die Mechaniken spielerisch Schritt fÃ¼r Schritt. Tutorials kÃ¶nnen jederzeit Ã¼ber TastendrÃ¼cke fortgeschritten oder pausiert werden. Der Fortschritt wird automatisch global gespeichert.

| Taste | Funktion |
| :--- | :--- |
| **Pfeil Auf/Ab** | Navigation in MenÃ¼s und Listen |
| **Pfeil Links/Rechts** | Werte anpassen (Slider, LautstÃ¤rke) |
| **Enter** | Auswahl bestÃ¤tigen |
| **Backspace / Esc** | ZurÃ¼ck zum vorherigen MenÃ¼ |
| **S** | **Status-Ãœbersicht** (Forschungspunkte, Fans, Mitarbeiter) |
| **F** | **Finanz-Check** (Kontostand, Gewinnberichte) |
| **Leertaste / 0** | Zeit pausieren / Tutorial fortsetzen |
| **1, 2, 3** | Spielgeschwindigkeit (Normal, Schnell, Ultra) |
| **C** | Crunch-Modus (wÃ¤hrend der Entwicklung) |

## ðŸ›  Features
- **KI-Pressekritiken**: Dynamische Reviews, die auf deine Statistiken reagieren.
- **Fan-System & Hype**: Messeauftritte, Bug-Reports und Community-Management.
- **Wirtschafts-Simulation**: Kredite, Aktienmarkt, Lizenzen und FirmenÃ¼bernahmen.
- **Mod-Support**: Erstelle eigene Themen und Genres ganz einfach ohne Internetverbindung.
- **Multilingual**: Volle UnterstÃ¼tzung fÃ¼r Deutsch und Englisch.

## ðŸ”§ Installation
### Windows
- Entpacke die `.zip` und starte `Audio_Studio_Tycoon_v3.11.0-beta.1.exe`.
- Dein Screenreader (NVDA, Jaws, SAPI) wird automatisch erkannt.

### Linux
- **Starten:** Nutze das `Audio_Studio_Tycoon_Linux.sh` Skript zum Starten des Spiels. Fǟr die Screenreader-Unterstǟtzung unter Linux nutzt `Tolk` den Speech Dispatcher (`speechd`). Stelle sicher, dass `speechd` installiert und aktiv ist, damit die akustischen Feedbacks funktionieren.
- **Kompilieren:** Um das Spiel nativ unter Linux zu kompilieren, fǟhre das mitgelieferte Skript `./build_linux.sh` aus. Dieses nutzt PyInstaller und generiert die ausfǟhrbare Datei im `dist/`-Verzeichnis.

---
*Entwickelt mit Leidenschaft fÃ¼r Barrierefreiheit.*


### v3.15 (New Features)
- **Influencer-Skandale:** Eine brandneue Event-Kette für gesponserte Streamer! Es gibt ein wöchentliches Risiko, dass der Streamer live vor laufender Kamera Mist baut (z.B. Cheats verwendet). Du erhältst eine Notfallmeldung und musst sofort das Krisenmanagement übernehmen: Öffentliche Entschuldigung, den Streamer teuer feuern, oder ignorieren und hoffen, dass es gut geht!

### v3.14 (New Features)
- **KI-Generierte Assets:** Spiele in der Entwicklung können jetzt massiv beschleunigt werden, indem die Entwickler auf KI-Assets zurückgreifen. Das spart Zeit und Budget, aber Vorsicht: Bei Release besteht eine 30%ige Chance, dass das Spiel wegen Urheberrechtsverletzungen von einer Anwaltskanzlei auf 500.000 € verklagt wird, was die Kritikerwertung und die Fan-Basis stark beschädigt!

### v3.13 (New Features)
- **Anti-Cheat System:** F2P-Titel und MMOs werden ab sofort von Cheater-Wellen heimgesucht, die Spieler vergraulen und Fans kosten! Der Kauf eines teuren Anti-Cheat-Systems (100.000 €) für jedes betroffene Spiel ist nun ein essentielles Management-Tool.
- **Filmlizenzen verkaufen:** Wenn ein Spiel ein Kritikererfolg (Score >= 8.0) und ein Verkaufsschlager (>= 500k Verkäufe) ist, können nun die Filmrechte an Hollywood verkauft werden für einen gigantischen Payout und noch mehr Fans!
- **Lootboxen & Mikrotransaktionen (MTX):** Füge bestehenden Spielen Lootboxen hinzu, um fortlaufende wöchentliche Einnahmen zu generieren. Aber Vorsicht: Die Community wird das nicht mögen und mit massiven Shitstorms und Fan-Verlusten reagieren!

### v3.12 (New Features)
- **In-Game Werbung:** Optional aktivierbar für veröffentlichte Spiele, um zusätzliche Einnahmen zu generieren (auf Kosten von Hype).
- **Modding-Support:** Reduziert den Verkaufsrückgang für Spiele und verlängert deren Lebensdauer auf dem Markt.
- **Phase 2 - Free-to-Play:** Entwickle Spiele als Free-to-Play mit Mikrotransaktionen für wöchentliches passives Einkommen, abhängig von der aktiven Spielerbasis.
- **Phase 2 - Remakes:** Wähle Spiele, die älter als 10 Jahre sind, und entwickle Remakes, um Nostalgie-Verkaufs-Boosts zu erhalten!
- **Phase 2 - Mergers & Acquisitions (M&A):** Kaufe rivalisierende Studios auf, profitiere von deren Katalog durch wöchentliche Dividenden und eliminiere die Konkurrenz.

