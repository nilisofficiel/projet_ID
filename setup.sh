#!/bin/bash

# Setup script for Animated Reality Show project
# This script automates the initial setup process

set -e  # Exit on error

echo "========================================"
echo "Animated Reality Show - Setup Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher first"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed"
    echo "Please install pip first"
    exit 1
fi

echo "✓ pip found"
echo ""

# Create virtual environment (optional but recommended)
read -p "Create a virtual environment? (recommended) [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
    echo "To activate it, run:"
    echo "  source venv/bin/activate  # On Linux/Mac"
    echo "  venv\\Scripts\\activate     # On Windows"
    echo ""
fi

# Install Python dependencies
echo "Installing Python dependencies..."
if command -v pip &> /dev/null; then
    pip install -r requirements.txt
else
    pip3 install -r requirements.txt
fi
echo "✓ Python dependencies installed"
echo ""

# Check if FFmpeg is installed
echo "Checking for FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✓ FFmpeg is installed"
else
    echo "⚠ FFmpeg is not installed"
    echo ""
    echo "FFmpeg is required for video editing. To install:"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo "  Windows: Download from https://ffmpeg.org/download.html"
    echo ""
fi

# Setup .env file
if [ ! -f .env ]; then
    echo "Setting up .env file..."
    cp .env.template .env
    echo "✓ .env file created from template"
    echo ""
    echo "⚠ IMPORTANT: Edit .env and add your API keys:"
    echo "  - HUGGINGFACE_API_KEY (get from https://huggingface.co/settings/tokens)"
    echo "  - DID_API_KEY (get from https://studio.d-id.com/account-settings)"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

# Create output directories
echo "Creating output directories..."
mkdir -p output/avatars
mkdir -p output/animations
mkdir -p output/episodes
mkdir -p projects
echo "✓ Output directories created"
echo ""

# Run verification
echo "Running installation verification..."
echo ""
python3 verify_installation.py

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your API keys"
echo "  2. Read QUICKSTART.md for a quick tutorial"
echo "  3. Try: python3 Scripts/examples.py"
echo ""
