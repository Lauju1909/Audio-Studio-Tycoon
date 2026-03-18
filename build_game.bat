@echo off
echo ========================================
echo AUDIO STUDIO TYCOON - BUILD STARTER
echo ========================================
echo.
echo Dieses Skript erstellt die neue Version 2.7.0.
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
echo ERFOLG: Die Datei Audio_Studio_Tycoon_v2.7.0.zip wurde erstellt!
pause
