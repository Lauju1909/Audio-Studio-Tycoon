@echo off
echo ========================================
echo AUDIO STUDIO TYCOON - BUILD STARTER
echo ========================================
echo.
echo Dieses Skript erstellt den Build basierend auf version.json.
echo Bitte stelle sicher, dass Python und PyInstaller installiert sind.
echo.
python tools/build_release.py
if errorlevel 1 (
    echo.
    echo FEHLER: Der Build-Prozess ist fehlgeschlagen.
    pause
    exit /b 1
)
echo.
echo ERFOLG: Der Build wurde in den Ordner 'releases' erstellt und gepackt!
pause
