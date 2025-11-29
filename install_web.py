#!/usr/bin/env python3
"""
Web-accessible installation script
This version outputs HTML for web browser viewing
Run this from your web browser or cPanel file manager
"""

import sys
import os
import subprocess
import platform
from datetime import datetime

def html_header():
    """Generate HTML header"""
    return """<!DOCTYPE html>
<html>
<head>
    <title>Package Installation - Console App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .info { color: #2196F3; }
        .success { color: #4CAF50; font-weight: bold; }
        .error { color: #f44336; font-weight: bold; }
        .warning { color: #FF9800; }
        pre {
            background: #f5f5f5;
            padding: 10px;
            border-radius: 3px;
            overflow-x: auto;
        }
        h1 { color: #333; }
        .footer { margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; }
    </style>
</head>
<body>
<div class="container">
    <h1>Console App - Package Installation</h1>
    <p><strong>Started:</strong> """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    <hr>
"""

def html_footer():
    """Generate HTML footer"""
    return """
    <div class="footer">
        <p><strong>Completed:</strong> """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        <p><em>If installation was successful, restart your Passenger application in cPanel.</em></p>
    </div>
</div>
</body>
</html>
"""

def print_html(message, status="info"):
    """Print HTML formatted message"""
    css_class = {
        "info": "info",
        "success": "success",
        "error": "error",
        "warning": "warning"
    }.get(status, "info")
    
    print(f'<p class="{css_class}">{message}</p>')
    sys.stdout.flush()

def main():
    """Main installation function - web version"""
    print(html_header())
    
    print_html("Starting package installation...", "info")
    print_html(f"Python version: {sys.version}", "info")
    print_html(f"Platform: {platform.platform()}", "info")
    print_html(f"Current directory: {os.getcwd()}", "info")
    print("<hr>")
    
    # Find requirements file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    version_info = sys.version_info
    
    requirements_file = os.path.join(script_dir, "requirements.txt")
    if version_info.major == 3 and version_info.minor == 7:
        py37_file = os.path.join(script_dir, "requirements-py37.txt")
        if os.path.exists(py37_file):
            requirements_file = py37_file
            print_html("Python 3.7 detected - using requirements-py37.txt", "info")
    
    if not os.path.exists(requirements_file):
        print_html(f"ERROR: Requirements file not found: {requirements_file}", "error")
        print(html_footer())
        return False
    
    print_html(f"Using requirements file: {os.path.basename(requirements_file)}", "info")
    print("<hr>")
    
    # Check pip
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print_html(f"pip found: {result.stdout.strip()}", "success")
        else:
            print_html("pip not available", "error")
            print(html_footer())
            return False
    except Exception as e:
        print_html(f"Error checking pip: {e}", "error")
        print(html_footer())
        return False
    
    print("<hr>")
    print_html("Upgrading pip...", "info")
    
    # Upgrade pip
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--user", "--upgrade", "pip"],
            capture_output=True,
            text=True,
            timeout=120
        )
        print_html("pip upgrade completed", "success")
    except Exception as e:
        print_html(f"pip upgrade warning: {e}", "warning")
    
    print("<hr>")
    print_html("Installing packages (this may take several minutes)...", "info")
    print("<pre>")
    sys.stdout.flush()
    
    # Install packages
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--user", "-r", requirements_file],
            capture_output=True,
            text=True,
            timeout=600
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        print("</pre>")
        
        if result.returncode == 0:
            print_html("✓ All packages installed successfully!", "success")
        else:
            print_html("Installation completed with warnings. Check output above.", "warning")
    except subprocess.TimeoutExpired:
        print("</pre>")
        print_html("Installation timed out. Please try again or install via SSH.", "error")
        print(html_footer())
        return False
    except Exception as e:
        print("</pre>")
        print_html(f"Error during installation: {e}", "error")
        print(html_footer())
        return False
    
    print("<hr>")
    print_html("Verifying installation...", "info")
    
    # Verify
    required_packages = ["fastapi", "uvicorn", "sqlalchemy", "pydantic", "asgiref"]
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_html(f"✓ {package} is installed", "success")
        except ImportError:
            print_html(f"✗ {package} is NOT installed", "error")
            missing.append(package)
    
    if missing:
        print_html(f"Missing packages: {', '.join(missing)}", "error")
        print_html("You may need to restart your application or check Python path", "warning")
    else:
        print_html("All required packages are installed!", "success")
    
    print(html_footer())
    return len(missing) == 0

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_html(f"Unexpected error: {e}", "error")
        import traceback
        print("<pre>")
        traceback.print_exc()
        print("</pre>")

