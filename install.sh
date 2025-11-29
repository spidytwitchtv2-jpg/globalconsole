#!/bin/bash
# Installation script for Namecheap server
# This script helps install Python packages correctly

echo "=========================================="
echo "Console App - Installation Script"
echo "=========================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Script directory: $SCRIPT_DIR"
echo ""

# Change to script directory
cd "$SCRIPT_DIR" || exit 1

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt not found in current directory!"
    echo "Current directory: $(pwd)"
    echo "Files in current directory:"
    ls -la
    exit 1
fi

echo "Found requirements.txt"
echo "Current directory: $(pwd)"
echo ""

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "ERROR: Python not found!"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "Python version: $PYTHON_VERSION"
echo ""

# Check pip version
echo "Checking pip version..."
if command -v pip3 &> /dev/null; then
    pip3 --version
elif command -v pip &> /dev/null; then
    pip --version
else
    echo "ERROR: pip not found!"
    exit 1
fi
echo ""

# Detect Python version and choose appropriate requirements file
PYTHON_MAJOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.minor)")

REQUIREMENTS_FILE="requirements.txt"

if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]; then
    echo "Python 3.7 detected - using Python 3.7 compatible requirements"
    REQUIREMENTS_FILE="requirements-py37.txt"
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        echo "⚠ Warning: $REQUIREMENTS_FILE not found, using requirements.txt"
        REQUIREMENTS_FILE="requirements.txt"
    fi
fi

echo "Using requirements file: $REQUIREMENTS_FILE"
echo ""

# Install packages
echo "Installing Python packages..."
echo "This may take a few minutes..."
echo ""

# Try different installation methods
if $PIP_CMD install --user -r "$REQUIREMENTS_FILE"; then
    echo ""
    echo "✓ Packages installed successfully!"
elif python3 -m pip install --user -r "$REQUIREMENTS_FILE"; then
    echo ""
    echo "✓ Packages installed successfully!"
else
    echo ""
    echo "⚠ Installation failed with first method, trying alternative..."
    $PIP_CMD install --user --upgrade pip
    if $PIP_CMD install --user -r "$REQUIREMENTS_FILE"; then
        echo ""
        echo "✓ Packages installed successfully!"
    else
        echo ""
        echo "❌ ERROR: Installation failed!"
        echo "Please check the error messages above and try manual installation."
        exit 1
    fi
fi

echo ""
echo "Verifying installation..."
if $PYTHON_CMD -c "import fastapi; print('✓ FastAPI installed')" 2>/dev/null; then
    echo "✓ Installation verified!"
else
    echo "⚠ Warning: FastAPI import test failed"
    echo "You may need to add Python user site-packages to your path"
fi

echo ""
echo "=========================================="
echo "Installation complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Restart your Passenger application in cPanel"
echo "2. Or create/update tmp/restart.txt file"
echo ""

