@echo off
chcp 65001 >nul
echo Audio Studio Tycoon v4.3.0 (Native Rust Edition) wird gestartet...
if exist "Audio_Studio_Tycoon.exe" (
    "Audio_Studio_Tycoon.exe"
) else (
    cargo run --release
)
