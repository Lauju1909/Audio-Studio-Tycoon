@echo off
chcp 65001 >nul
echo ========================================================
echo AUDIO STUDIO TYCOON v4.3.0 (RUST EDITION) - BUILD & TEST
echo ========================================================
echo.
echo [1/3] Starte automatisierte Rust-Testsuite (cargo test)...
cargo test
if errorlevel 1 (
    echo.
    echo FEHLER: Tests fehlgeschlagen!
    pause
    exit /b 1
)
echo.
echo [2/3] Kompiliere hochoptimierte 64-Bit Native Release-Exe...
cargo build --release
if errorlevel 1 (
    echo.
    echo FEHLER: Kompilierung fehlgeschlagen!
    pause
    exit /b 1
)
copy /Y "target\release\audio_studio_tycoon.exe" "Audio_Studio_Tycoon.exe" >nul
echo.
echo [3/3] Prüfe End-to-End Simulation (--verify)...
"Audio_Studio_Tycoon.exe" --verify
echo.
echo ERFOLG: Audio_Studio_Tycoon.exe wurde erfolgreich kompiliert und verifiziert!
pause
