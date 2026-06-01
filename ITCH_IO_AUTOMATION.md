# Leitfaden zur Automatisierung von itch.io Uploads für Audio Studio Tycoon

Dieser Leitfaden erklärt, wie du mich (die KI) befähigen kannst, dein Spiel "Audio Studio Tycoon" automatisch zu bauen, zu verpacken und direkt auf itch.io hochzuladen.

## 1. Was ist das `butler` CLI-Tool?

`butler` ist das offizielle Kommandozeilen-Tool von itch.io. Es wurde speziell dafür entwickelt, Spiele effizient und zuverlässig auf die Plattform hochzuladen. Anstatt jedes Mal manuell eine ZIP-Datei über die Webseite hochzuladen, kann `butler` die Dateien analysieren, nur die Änderungen (Patches) hochladen und den gesamten Prozess automatisieren. Das macht es ideal für uns, um Uploads direkt aus dem Code-Editor heraus zu erledigen.

## 2. Einrichtung: So machst du `butler` startklar

Damit ich `butler` für dich nutzen kann, musst du es einmalig auf deinem System einrichten:

1.  **Herunterladen:** Lade dir das `butler` Tool für Windows von der offiziellen itch.io Seite herunter (suche einfach nach "itch.io butler download").
2.  **Entpacken und im PATH hinterlegen:** Entpacke die heruntergeladene Datei (z.B. nach `C:\butler`). Damit ich den Befehl überall ausführen kann, musst du diesen Ordner zu deinen Windows-Umgebungsvariablen (`PATH`) hinzufügen.
3.  **Einmalig einloggen:** Öffne dein Terminal (PowerShell oder Eingabeaufforderung) und führe folgenden Befehl aus:
    ```bash
    butler login
    ```
    Es öffnet sich dein Browser. Bestätige dort die Anmeldung mit deinem itch.io Account.

Sobald das erledigt ist, ist `butler` auf deinem Computer einsatzbereit!

## 3. Wie du mich beauftragst (Prompt-Beispiele)

Wenn `butler` eingerichtet ist, kannst du mir einfach sagen, dass ich das Spiel hochladen soll. Da ich Zugriff auf dein System habe, kann ich die entsprechenden Befehle für dich ausführen.

Hier sind Beispiele, wie du mir den Auftrag geben kannst:

*   *"Baue die aktuelle Version von Audio Studio Tycoon mit PyInstaller. Erstelle eine ZIP-Datei `Audio_Studio_Tycoon_v1.5.zip` und lade den Build-Ordner mit butler auf meine itch.io Seite `Lauju1909/audio-studio-tycoon:windows` hoch."*
*   *"Die Tests sind erfolgreich. Bitte kompiliere das Spiel für Windows und nutze butler, um das Update direkt auf itch.io (Lauju1909/audio-studio-tycoon) zu pushen."*
*   *"Lade den aktuellen Stand aus dem Ordner `dist/Audio_Studio_Tycoon` mit butler als neuen Windows-Build auf Lauju1909/audio-studio-tycoon hoch."*

Ich werde dann den Befehl in etwa so ausführen:
`butler push dist/Audio_Studio_Tycoon Lauju1909/audio-studio-tycoon:windows`

## 4. Sicherheit: Dein Passwort bleibt sicher

Du musst dir keine Sorgen um deine Zugangsdaten machen. Du musst mir **niemals** dein itch.io Passwort im Klartext geben!

Der Befehl `butler login`, den du selbst ausführst, speichert ein sicheres Authentifizierungs-Token auf deinem Computer. Wenn ich später den `butler push` Befehl ausführe, nutzt das Tool automatisch dieses gespeicherte Token. Ich kenne dein Passwort nicht und brauche es auch nicht. Deine Zugangsdaten bleiben lokal und sicher bei dir.
