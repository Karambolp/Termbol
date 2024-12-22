#!/bin/bash

echo -e "\e[36mTermbol AI Terminal Uninstaller\e[0m"
echo "===================================="
echo -e "\e[35mDeveloped by Karambol (https://github.com/Karambolp)\e[0m\n"

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "\e[31mError: Please run as root (use sudo)\e[0m"
    exit 1
fi

# Installation directories
INSTALL_DIR="/opt/termbol"
BIN_DIR="/usr/local/bin"

echo -e "\n\e[34m[1/2]\e[0m Removing program files..."
rm -f "$BIN_DIR/termbol"
rm -rf "$INSTALL_DIR"

echo -e "\e[34m[2/2]\e[0m Cleaning up Python packages..."
pip3 uninstall -y -r requirements.txt > /dev/null 2>&1 || echo -e "\e[33mWarning: Could not uninstall Python packages\e[0m"

echo -e "\n\e[32m✓ Uninstallation completed!\e[0m"