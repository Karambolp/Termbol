#!/bin/bash

echo -e "\e[36mTermbol AI Terminal Installer\e[0m"
echo "=================================="
echo -e "\e[35mDeveloped by Karambol (https://github.com/Karambolp)\e[0m\n"

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "\e[31mError: Please run as root (use sudo)\e[0m"
    exit 1
fi

# Installation directory
INSTALL_DIR="/opt/termbol"
BIN_DIR="/usr/local/bin"

# Create installation directory
echo -e "\n\e[34m[1/6]\e[0m Creating installation directory..."
mkdir -p "$INSTALL_DIR"

# Copy files
echo -e "\e[34m[2/6]\e[0m Copying files..."
cp main.py "$INSTALL_DIR/"
cp requirements.txt "$INSTALL_DIR/" 2>/dev/null || echo -e "\e[33mWarning: requirements.txt not found\e[0m"

# Install required system packages
echo -e "\e[34m[3/6]\e[0m Installing system packages..."
apt-get update -qq
apt-get install -y python3 python3-pip > /dev/null 2>&1

# Install Python packages
echo -e "\e[34m[4/6]\e[0m Installing Python packages..."
pip3 install -r requirements.txt > /dev/null 2>&1 || echo -e "\e[33mWarning: Could not install Python packages\e[0m"

# Get API Key
echo -e "\n\e[34m[5/6]\e[0m Setting up Google Gemini API Key"
echo "=================================="
echo -e "1. Go to \e[36mhttps://aistudio.google.com\e[0m"
echo "2. Sign in with your Google account"
echo "3. Click 'Create API key'"
echo "4. Copy the generated API key"
echo -e "\n🔑 Paste your API key:"
read -p "> " API_KEY

# Create .env file
echo -e "\e[34m[6/6]\e[0m Creating configuration files..."
cat > "$INSTALL_DIR/.env" << EOF
# Gemini API Key
# -------------
GEMINI_API_KEY=$API_KEY

# Save Directory
# -------------
SAVE_DIR=~/Documents/termbol_saves
EOF

# Create executable script
echo -e "Creating executable..."
cat > "$BIN_DIR/termbol" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
python3 main.py "\$@"
EOF

# Set permissions
echo -e "Setting permissions..."
chmod +x "$BIN_DIR/termbol"
chmod 644 "$INSTALL_DIR/main.py"
chmod 600 "$INSTALL_DIR/.env"

echo -e "\n\e[32m✓ Installation completed!\e[0m"
echo -e "\e[36mUse 'termbol --help' to see available commands\e[0m"