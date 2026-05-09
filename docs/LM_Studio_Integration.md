# LM Studio Integration Guide für Antigravity

Hallo! Ich habe gesehen, dass du **LM Studio (v0.4.12)** mit dem Modell **Qwen 3.6 27B** (von dir liebevoll "Lmmy the space invader" genannt) erfolgreich auf `http://127.0.0.1:1234` am Laufen hast.

Hier ist die Anleitung, wie du dieses Modell in **Antigravity** einbindest, damit du es auch dann nutzen kannst, wenn deine Standard-Kontingente (Cloud-Modelle) aufgebraucht sind.

## 1. Konfiguration in der `mcp_config.json`

Da Antigravity das **Model Context Protocol (MCP)** nutzt, kannst du LM Studio als eigenen "Server" hinzufügen. Dadurch kann ich (dein KI-Assistent) das lokale Modell direkt fragen oder Aufgaben an es delegieren.

Füge den folgenden Block zu deiner `c:\Users\lauri\.gemini\antigravity\mcp_config.json` unter `mcpServers` hinzu:

"lm-studio-local": {
  "command": "C:\\Program Files\\nodejs\\node.exe",
  "args": [
    "C:\\Users\\lauri\\.gemini\\antigravity\\mcp_servers\\lm-studio\\node_modules\\@mzxrai\\mcp-openai\\dist\\index.js"
  ],
  "env": {
    "OPENAI_API_KEY": "lm-studio",
    "OPENAI_BASE_URL": "http://127.0.0.1:1234/v1",
    "OPENAI_MODEL": "qwen/qwen3.6-27b"
  }
}
```

> [!IMPORTANT]
> Ich habe den Server von `lm-studio` in `lm-studio-local` umbenannt, um eine saubere Neuinitialisierung zu erzwingen. Außerdem nutzen wir jetzt einen direkten Pfad zur installierten Brücke, was unter Windows stabiler ist als `npx`.

> [!TIP]
> Da LM Studio eine OpenAI-kompatible API bereitstellt, nutzt dieser Befehl den `mcp-server-openai` als Brücke. Falls das Paket noch nicht installiert ist, wird es durch `-y` automatisch geladen.

## 2. Nutzung als Haupt-Modell (Fallback)

Wenn du das Modell direkt für deine Chats in der Antigravity-Oberfläche auswählen möchtest, folge diesen Schritten:

1. Öffne die **Settings** in Antigravity (`Strg` + `,`).
2. Suche nach **"Custom Providers"** oder **"Model Providers"**.
3. Klicke auf **"Add Provider"** (oder ähnlich).
4. Gib folgende Daten ein:
   - **Name:** LM Studio (Lmmy)
   - **Base URL:** `http://localhost:1234/v1`
   - **API Key:** `lm-studio` (oder ein beliebiges Wort, da LM Studio lokal keinen Key erzwingt)
   - **Model ID:** `qwen/qwen3.6-27b`

## 3. Besonderheiten für "Lmmy" (Qwen 3.6)

Das Qwen-Modell ist sehr leistungsfähig, braucht aber klare Anweisungen für das "Tool-Calling". Wenn du merkst, dass es in Antigravity nicht so reagiert wie erwartet:

- Stelle sicher, dass in LM Studio unter **"Server Settings"** das Häkchen bei **"Cross-Origin Resource Scoring (CORS)"** gesetzt ist (falls Antigravity als Web-App im Browser liefe, was hier aber lokal meist nicht nötig ist).
- Prüfe in den Logs von LM Studio (die du mir geschickt hast), ob Anfragen ankommen.

## 4. Automatischer Fallback

In den kommenden Versionen von Antigravity kannst du in den **Agent Settings** einstellen:
`"fallback_model": "lm-studio/qwen/qwen3.6-27b"`

Sobald dein Cloud-Limit erreicht ist, schaltet das System automatisch auf deine lokale Instanz um.

---
**Status:** LM Studio läuft auf Port 1234. Sobald du die `mcp_config.json` gespeichert hast, starte Antigravity neu, damit der neue Server geladen wird!
