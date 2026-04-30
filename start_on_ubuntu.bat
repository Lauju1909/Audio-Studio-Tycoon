@echo off
echo ========================================
echo Audio Studio Tycoon - WSL Ubuntu Starter
echo ========================================
echo.
echo Starte das Spiel in der Ubuntu-Umgebung...
echo (Stelle sicher, dass WSLg oder ein Sound-Server aktiv ist)
echo.

wsl -d Ubuntu python3 /mnt/c/Users/lauri/.gemini/antigravity/scratch/game_dev_tycoon_2/main.py

if errorlevel 1 (
    echo.
    echo Fehler beim Starten in WSL. 
    echo Moeglicherweise fehlen Abhaengigkeiten.
    echo Versuche: wsl -d Ubuntu pip3 install pygame --break-system-packages
    pause
)
pause
