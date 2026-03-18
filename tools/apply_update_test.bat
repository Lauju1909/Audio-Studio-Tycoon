@echo off
echo Entpacke Update in temporaeren Ordner...
if exist "update_temp" rmdir /s /q "update_temp"
mkdir "update_temp"
powershell -Command "Expand-Archive -Force -Path 'update.zip' -DestinationPath 'update_temp'" 
del "update.zip"
echo Kopiere neue Dateien...
xcopy /s /e /y "update_temp\*" "."
rmdir /s /q "update_temp"
echo Suche nach der neuen exe...
for /f "delims=" %%I in ('dir /b Audio_Studio_Tycoon_v*.exe Audio_Studio_Tycoon_*.exe 2^>nul') do set "NEW_EXE=%%I"
if defined NEW_EXE (
    echo FOUND EXE: %NEW_EXE%
) else (
    echo NO EXE FOUND!
)
