@echo off
echo ========================================
echo Audio Studio Tycoon - WSL Setup
echo ========================================
echo.
echo Installiere Pygame und Speech-Dispatcher in Ubuntu...
echo.

wsl -d Ubuntu pip3 install pygame --break-system-packages
echo.
echo Fuer die Sprachausgabe (speechd) ist sudo-Zugriff in Ubuntu erforderlich.
echo Bitte gib dein Passwort in der Ubuntu-Konsole ein, falls gefragt.
echo.
wsl -d Ubuntu sudo apt-get update
wsl -d Ubuntu sudo apt-get install -y python3-speechd speech-dispatcher

echo.
echo Setup abgeschlossen! Du kannst nun start_on_ubuntu.bat nutzen.
pause
