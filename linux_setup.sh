#!/bin/bash
echo "========================================"
echo "Audio Studio Tycoon - Linux Setup"
echo "========================================"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python 3 is not installed. Please install it first."
    exit
fi

echo "Installing dependencies..."
# Install pygame and speechd wrapper
sudo apt-get update
sudo apt-get install -y python3-pip python3-pygame python3-speechd speech-dispatcher

# Optional: Install pip requirements if a requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
else
    pip3 install pygame
fi

echo ""
echo "Setup complete!"
echo "You can now start the game with: python3 main.py"
echo ""
echo "Make sure your screen reader (Orca) is active."
