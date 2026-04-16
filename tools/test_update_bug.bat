@echo off
setlocal
echo 1. Entpacken...
if exist update_temp rmdir /s /q update_temp
powershell -Command "Expand-Archive -Force -LiteralPath 'Audio_Studio_Tycoon_v2.7.1.zip' -DestinationPath 'update_temp'"
echo 2. Finde SRC_DIR
set "SRC_DIR=update_temp"
for /d %%D in ("update_temp\*") do (
    if exist "%%D\Audio_Studio_Tycoon_*.exe" set "SRC_DIR=%%D"
)
echo SRC_DIR ist: %SRC_DIR%
echo 3. Kopieren...
xcopy /s /e /y /c "%SRC_DIR%\*" "." > copy_log.txt
echo 4. Suchen...
for /f "delims=" %%I in ('dir /b Audio_Studio_Tycoon_v*.exe Audio_Studio_Tycoon_*.exe 2^>nul') do (
    echo Gesehen: %%I
    set "NEW_EXE=%%I"
)
if defined NEW_EXE (
    echo FOUND: %NEW_EXE%
) else (
    echo NOT FOUND!
)
endlocal
