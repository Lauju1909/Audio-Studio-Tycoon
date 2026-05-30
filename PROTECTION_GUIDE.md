# Audio Studio Tycoon - Leitfaden zum Schutz vor Piraterie und Code-Diebstahl

Dieser Leitfaden behandelt die wichtigsten Aspekte der Spielsicherheit für dein Python-Projekt, wenn du es auf Plattformen wie itch.io veröffentlichst.

## 1. PyInstaller: Bündelung ist kein Schutz
Du nutzt bereits **PyInstaller**, um dein Spiel in eine ausführbare `.exe`-Datei zu packen. Es ist wichtig zu verstehen, dass PyInstaller den Code **nicht** vor Reverse Engineering schützt. Er bündelt lediglich den Python-Interpreter und deine `.pyc` (oder `.py`)-Dateien.
Mit Tools wie *PyInstxtractor* und *uncompyle6* kann fast jeder mit etwas technischem Wissen deine `.exe` wieder entpacken und den originalen Quellcode auslesen. Betrachte PyInstaller also nur als Verteilungswerkzeug, nicht als Sicherheitsmaßnahme.

## 2. Code-Verschleierung und Kompilierung
Um es Angreifern deutlich schwerer zu machen, deinen Code zu stehlen oder zu manipulieren, kannst du folgende Tools einsetzen:

### PyArmor
**PyArmor** ist ein Kommandozeilen-Tool, das Python-Skripte verschleiert (obfuscated) und an bestimmte Laufzeitumgebungen bindet.
- **Wie es funktioniert:** Es transformiert deinen Code in eine unleserliche Form und verschlüsselt ihn. Erst zur Laufzeit wird er im Speicher entschlüsselt.
- **Vorteile:** Sehr starker Schutz für Python-Code, einfach in bestehende PyInstaller-Workflows zu integrieren.
- **Nachteile:** Kann manchmal von Antivirenprogrammen als verdächtig eingestuft werden (False Positives).

### Cython
Mit **Cython** kannst du deinen Python-Code in C-Code übersetzen und anschließend zu nativen, kompilierten Binärdateien (`.pyd` unter Windows, `.so` unter Linux) kompilieren.
- **Vorteile:** Aus C-Code erstellte Maschinensprache ist extrem schwer zu dekompilieren (Reverse Engineering). Oft gibt es sogar einen leichten Leistungsschub.
- **Nachteile:** Erfordert einen C-Compiler auf deinem System und einen zusätzlichen Build-Schritt.

## 3. Schutz von Assets (Audiodateien)
Für ein Audio-Spiel sind die Sound-Assets besonders wertvoll. Wenn sie einfach als `.wav`- oder `.mp3`-Dateien in einem Ordner liegen, können sie problemlos kopiert werden.

- **Verschlüsselung:** Du kannst die Audiodateien mit einem einfachen Algorithmus (z. B. AES) verschlüsseln und sie erst zur Laufzeit im Speicher (RAM) entschlüsseln, bevor sie abgespielt werden. Bibliotheken wie `cryptography` können hier helfen.
- **Asset-Archive (WAD/PAK):** Anstatt viele Einzeldateien auszuliefern, packst du alle Sounds in eine einzige große Archivdatei und liest die Byte-Streams direkt aus dieser Datei aus.
- **PyInstaller Bundling:** Du kannst Assets auch in die `.exe` mit PyInstaller einbinden (mit der Option `--add-data`). Dies verhindert jedoch nur das zufällige Kopieren durch Laien, da Tools wie PyInstxtractor diese Dateien wieder extrahieren können.

## 4. Reality Check: Lohnt sich aggressiver Schutz?
Für ein Indie-Audiogame solltest du die Maßnahmen kritisch abwägen. Aggressives DRM (Digital Rights Management) und Obfuskation können erhebliche Nachteile haben:

- **Antiviren-Probleme (False Positives):** Verschleierter Code und verschlüsselte Assets werden von Windows Defender und anderen AV-Scannern oft als Malware eingestuft. Das frustriert ehrliche Käufer.
- **Barrierefreiheit (Accessibility):** Für ein voll zugängliches Audio-Spiel ist es extrem wichtig, dass Screenreader (über Tolk oder SAPI) fehlerfrei arbeiten. Aggressive Anti-Cheat- oder Anti-Debugging-Tools können in diese System-APIs eingreifen und den Screenreader blockieren oder das Spiel abstürzen lassen.
- **Die Realität der Piraterie:** Raubkopierer, die wirklich wollen, finden fast immer einen Weg. Eine zu starke Gängelung trifft oft die ehrlichen Spieler (durch Performance-Einbußen oder blockierte Software) härter als die eigentlichen Piraten.

**Empfehlung:** Setze auf einen mittleren Schutz. Nutze Cython für die wichtigsten Logik-Dateien oder ein leichtes PyArmor-Setup, um Gelegenheitsdiebe abzuschrecken. Verstecke die Sounds in Archiven, aber verzichte auf komplexe Laufzeit-Entschlüsselung, wenn diese die Performance deines Screenreaders beeinträchtigt.
