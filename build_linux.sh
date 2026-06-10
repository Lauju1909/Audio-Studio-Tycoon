#!/bin/bash
set -e

echo "Building Audio Studio Tycoon for Linux..."

# Install PyInstaller if not already installed
pip install pyinstaller

# Run pyinstaller with the Linux spec file
pyinstaller --clean Audio_Studio_Tycoon_Linux.spec

VERSION=$(grep '"version":' version.json | cut -d '"' -f 4)
mv dist/Audio_Studio_Tycoon_Linux "dist/Audio_Studio_Tycoon_v${VERSION}"
zip -r "releases/Audio_Studio_Tycoon_v${VERSION}.zip" "dist/Audio_Studio_Tycoon_v${VERSION}"

echo "Build complete. Check the 'dist' directory."
