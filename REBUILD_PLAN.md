# Rebuild-Plan (Audio Studio Tycoon)

Backup: git tag `pre-rebuild-backup` (PC d8834dd, Android 00645df). Restore: `git checkout pre-rebuild-backup`.
Baseline: 124 pytest passed (py -3.13), 9 node simulation tests passed.

## Ist-Zustand
- logic.py 5736 Zeilen (Monolith), game_data.py ~137KB, models.py 1583 Zeilen, menus/ + managers/ bereits teilweise getrennt.
- Android: www/tycoon_engine.js (Logik), app.js (UI), sound.js/audio_engine.js.

## Ziel-Architektur (inkrementell, Tests bleiben gruen)
1. core/  : GameState (reine Daten, serialisierbar), Engine (tick/turn), EventBus. Keine pygame/Audio-Imports.
2. systems/: logic.py in Module je Domaene (dev, finance, hr, research, marketing, ...) zerlegen; logic.py bleibt als Fassade.
3. data/  : game_data.py in JSON/Module je Bereich + i18n (de/en) mit Paritaetstest.
4. ui/    : Menues nur Darstellung + Screenreader-Ansagen (prism.dll, explizite ctypes-Signaturen, nie is_speaking/get_volume).
5. Android: gleiche Schichtung (engine/ui/audio), danach `npx cap copy android`.
Regel pro Schritt: Modul extrahieren -> Fassade -> pytest + npm test -> Commit.
