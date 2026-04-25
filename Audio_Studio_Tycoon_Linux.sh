#!/bin/bash
# Audio Studio Tycoon - Linux "One-Click" Runner

# Farben für Feedback
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   Audio Studio Tycoon - Linux Runner   ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 1. Check for Python
if ! command -v python3 &> /dev/null
then
    echo -e "${RED}Fehler: Python 3 ist nicht installiert.${NC}"
    echo "Bitte installiere Python 3 (z.B. sudo apt install python3)"
    exit 1
fi

# 2. Check for dependencies (pygame & speechd)
MISSING_DEPS=false
python3 -c "import pygame" &> /dev/null || MISSING_DEPS=true
python3 -c "import speechd" &> /dev/null || MISSING_DEPS=true

if [ "$MISSING_DEPS" = true ]; then
    echo "Es fehlen notwendige Bibliotheken (Pygame/Speechd)."
    echo "Soll ich sie jetzt automatisch installieren? (Passwort erforderlich)"
    read -p "[J/n]: " choice
    if [[ "$choice" =~ ^[Nn]$ ]]; then
        echo "Abgebrochen. Das Spiel kann ohne diese Pakete nicht starten."
        exit 1
    fi
    
    # Installation
    echo "Starte Installation..."
    if [ -f /etc/debian_version ]; then
        sudo apt-get update
        sudo apt-get install -y python3-pygame python3-speechd speech-dispatcher
    elif [ -f /etc/fedora-release ]; then
        sudo dnf install -y python3-pygame python3-speech-dispatcher
    elif [ -f /etc/arch-release ]; then
        sudo pacman -S --noconfirm python-pygame speech-dispatcher
    else
        # Fallback auf Pip für Pygame
        pip3 install pygame --break-system-packages
    fi
fi

# 3. Spiel starten
echo -e "${GREEN}Starte Spiel...${NC}"
python3 main.py

if [ $? -ne 0 ]; then
    echo -e "${RED}Das Spiel wurde unerwartet beendet.${NC}"
    read -p "Druecke Enter zum Schliessen..."
fi
