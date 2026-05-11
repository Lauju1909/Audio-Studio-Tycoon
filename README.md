# Audio Studio Tycoon

> [!NOTE]
> **Lokale KI-Integration:** Dieses Projekt unterstützt nun die Anbindung an **LM Studio** als Fallback-KI. Den Guide dazu findest du in [docs/LM_Studio_Integration.md](docs/LM_Studio_Integration.md).

## Über das Spiel

Audio Studio Tycoon ist eine 100% Screenreader-optimierte Management-Simulation, bei der du deine eigene Spielefirma gründest. Entwickle Spiele, stelle Mitarbeiter ein und werde zum Tycoon der Branche!

## Features
- **Barrierefreiheit**: Vollständige Unterstützung für NVDA (Text-to-Speech) und Sound-Effekte.
- **Detaillierte Reviews**: Erhalte qualifiziertes Feedback von der Fachpresse. Dank **KI-Pressekritiken** sind diese dynamisch und passen sich deinen Spiele-Statistiken an.
- **Fan-System & Hype**: Kommuniziere mit deinen Fans über E-Mails, reagiere auf Bug-Reports und organisiere **Spiele-Messen**, um gigantischen Hype aufzubauen!
- **Service & Support**: Veröffentliche Patches und DLCs, oder baue dir ein passives Einkommen mit deinem eigenen **Abo-Service (Game Pass)** auf.
- **Plattform-Evolution**: Erlebe den Marktzyklus von Konsolen und PCs über Jahrzehnte.
- **Co-Development**: Entwickle Spiele zusammen mit Konkurrenten für massive Speed-Boosts bei 50/50 Profit Split.
- **Spionage & Sabotage**: Beauftrage Industriespione, um Tech-Daten zu stehlen, oder zerstöre den Ruf deiner Konkurrenz mit Schmutzkampagnen.
- **HR-Management**: Verwalte Mitarbeiter-Moral, Burnout, Gehaltsverhandlungen und verhindere, dass deine besten Entwickler kündigen!
- **Zweisprachig (DE/EN)**: Das gesamte Spiel, inklusive aller KI-Texte, lässt sich flexibel auf Deutsch oder Englisch spielen.

## Installation & Start

### Windows
1. Lade das aktuelle Release (`.zip` aus dem Releases-Tab) herunter und entpacke es.
2. Führe `Audio_Studio_Tycoon_v[Version].exe` aus.
3. Stelle sicher, dass dein Screenreader (z.B. NVDA) aktiv ist.

### Linux (Ubuntu, Debian, Fedora, Arch)
1. Lade das Linux-Release (`_Linux.zip`) herunter und entpacke es.
2. Mache den Runner ausführbar: `chmod +x Audio_Studio_Tycoon_Linux.sh`
3. Starte das Spiel: `./Audio_Studio_Tycoon_Linux.sh`
   *Das Skript prüft automatisch auf Abhängigkeiten (Pygame/Speechd) und installiert diese auf Wunsch.*

## Steuerung
- **Pfeiltasten**: Navigieren in Menüs und Slidern.
- **Enter**: Auswahl bestätigen.
- **Buchstaben**: Texteingabe für Firmen- und Spielnamen.

## Credits & Attribution
- **Sound Effects & Music** provided by Eric Matyas (www.soundimage.org)

## Neueste Änderungen (v3.6.1)
- **Sprachausgabe-Fix**:
    - Überarbeitung der `Tolk`- und `SAPI`-Integration für stabilere Audio-Ausgabe.
    - Fehler im COM-Threading behoben, der zu Abstürzen oder fehlender Sprachausgabe führen konnte.
    - Intelligente Erkennung: Screenreader aktiv (Tolk) vs. kein Screenreader (SAPI).
- **Hauptmenü-Integration (v3.6.0)**:
    - Das Monetarisierungs-Menü wurde in "Entwickler unterstützen" umbenannt.
    - Dynamische Rückkehr-Logik für das Support-Menü.
- **Gutschein-Support-System (v3.5.1)**:
    - Spieler können den Entwickler nun direkt unterstützen, indem sie Gutscheincodes (Google Play, Steam, Paysafecard) über das Spiel einsenden.
    - Automatisierte E-Mail-Vorbereitung an `lauju1909@gmail.com` nach Code-Eingabe.
- **Monetarisierungs-System (v3.5.0)**:
    - Neues Menü "Monetarisierung" unter Finanzen/Bank hinzugefügt.
    - **Werbung ansehen**: Spieler können einmal pro In-Game-Woche ein kurzes Werbevideo (simuliert) ansehen und dafür 5.000 € Belohnung erhalten.
    - **Entwickler unterstützen**: Direkter Link zur GitHub-Seite integriert, um das Projekt zu unterstützen.
- **Audio & Accessibility**: 
    - Integration der `Tolk`-Library für nahtlose Unterstützung aller gängigen Screenreader.
    - Akustische Warnungen bei kritischem Budget und Pleite-Check.
- **Fehlerbehebungen**: 
    - Stabilität des Speichersystems bei Büro-Objekten verbessert.
    - Bereinigung redundanter Logik-Events.

