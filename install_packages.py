#!/usr/bin/env python3
"""
Python Package Installation Script for Namecheap
Run this script to automatically install all required packages.
Can be executed via SSH or from application management page.
"""

import sys
import os
import subprocess
import platform

def print_status(message, status="INFO"):
    """Print colored status messages"""
    colors = {
        "INFO": "\033[94m",    # Blue
        "SUCCESS": "\033[92m", # Green
        "ERROR": "\033[91m",   # Red
        "WARNING": "\033[93m", # Yellow
        "RESET": "\033[0m"     # Reset
    }
    print(f"{colors.get(status, '')}[{status}]{colors['RESET']} {message}")

def get_python_version():
    """Get Python version info"""
    return sys.version_info

def find_requirements_file():
    """Find the appropriate requirements file based on Python version"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check Python version
    version_info = get_python_version()
    major, minor = version_info.major, version_info.minor
    
    # Default requirements file
    requirements_file = os.path.join(script_dir, "requirements.txt")
    
    # For Python 3.7, use the compatible version
    if major == 3 and minor == 7:
        py37_file = os.path.join(script_dir, "requirements-py37.txt")
        if os.path.exists(py37_file):
            requirements_file = py37_file
            print_status(f"Python 3.7 detected - using requirements-py37.txt", "INFO")
    
    if not os.path.exists(requirements_file):
        print_status(f"ERROR: Requirements file not found: {requirements_file}", "ERROR")
        return None
    
    return requirements_file

def check_pip_available():
    """Check if pip is available"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print_status(f"pip found: {result.stdout.strip()}", "SUCCESS")
            return True
    except Exception as e:
        print_status(f"Error checking pip: {e}", "ERROR")
    
    return False

def upgrade_pip():
    """Upgrade pip to latest version"""
    print_status("Upgrading pip...", "INFO")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--user", "--upgrade", "pip"],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            print_status("pip upgraded successfully", "SUCCESS")
            return True
        else:
            print_status(f"pip upgrade warning: {result.stderr}", "WARNING")
            return True  # Continue even if upgrade has warnings
    except Exception as e:
        print_status(f"Error upgrading pip: {e}", "WARNING")
        return False

def install_packages(requirements_file):
    """Install packages from requirements file"""
    print_status(f"Installing packages from {os.path.basename(requirements_file)}...", "INFO")
    print_status("This may take several minutes...", "INFO")
    
    try:
        # Install packages to user directory
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--user", "-r", requirements_file],
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        if result.returncode == 0:
            print_status("✓ All packages installed successfully!", "SUCCESS")
            return True
        else:
            print_status(f"Installation failed: {result.stderr}", "ERROR")
            print_status("Trying alternative installation method...", "WARNING")
            
            # Try without --user flag (might work in some environments)
            result2 = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", requirements_file],
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result2.returncode == 0:
                print_status("✓ Packages installed (without --user flag)", "SUCCESS")
                return True
            else:
                print_status(f"Alternative installation also failed: {result2.stderr}", "ERROR")
                return False
                
    except subprocess.TimeoutExpired:
        print_status("Installation timed out. This may take longer on slow connections.", "ERROR")
        return False
    except Exception as e:
        print_status(f"Error during installation: {e}", "ERROR")
        return False

def verify_installation():
    """Verify that key packages are installed"""
    print_status("Verifying installation...", "INFO")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "asgiref"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_status(f"✓ {package} is installed", "SUCCESS")
        except ImportError:
            print_status(f"✗ {package} is NOT installed", "ERROR")
            missing_packages.append(package)
    
    if missing_packages:
        print_status(f"Missing packages: {', '.join(missing_packages)}", "ERROR")
        return False
    else:
        print_status("All required packages are installed!", "SUCCESS")
        return True

def get_installation_path():
    """Get the path where packages are installed"""
    try:
        import site
        user_site = site.getusersitepackages()
        if user_site and os.path.exists(user_site):
            return user_site
        
        # Fallback to common location
        home = os.path.expanduser('~')
        version = f"{sys.version_info.major}.{sys.version_info.minor}"
        path = os.path.join(home, '.local', 'lib', f'python{version}', 'site-packages')
        if os.path.exists(path):
            return path
    except:
        pass
    return None

def main():
    """Main installation function"""
    print("=" * 60)
    print("Console App - Python Package Installer")
    print("=" * 60)
    print()
    
    # Print system information
    print_status(f"Python version: {sys.version}", "INFO")
    print_status(f"Platform: {platform.platform()}", "INFO")
    print_status(f"Current directory: {os.getcwd()}", "INFO")
    print_status(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}", "INFO")
    print()
    
    # Find requirements file
    requirements_file = find_requirements_file()
    if not requirements_file:
        print_status("Cannot proceed without requirements file", "ERROR")
        return False
    
    print_status(f"Using requirements file: {os.path.basename(requirements_file)}", "INFO")
    print()
    
    # Check pip availability
    if not check_pip_available():
        print_status("pip is not available. Please install pip first.", "ERROR")
        return False
    
    print()
    
    # Upgrade pip
    upgrade_pip()
    print()
    
    # Install packages
    if not install_packages(requirements_file):
        print_status("Package installation failed!", "ERROR")
        return False
    
    print()
    
    # Verify installation
    if not verify_installation():
        print_status("Installation verification failed!", "ERROR")
        print_status("You may need to restart your application or check Python path", "WARNING")
        return False
    
    print()
    print("=" * 60)
    print_status("Installation completed successfully!", "SUCCESS")
    print("=" * 60)
    print()
    
    # Show installation path
    install_path = get_installation_path()
    if install_path:
        print_status(f"Packages installed to: {install_path}", "INFO")
    
    print()
    print_status("Next steps:", "INFO")
    print("1. Restart your Passenger application in cPanel")
    print("2. Or create/update tmp/restart.txt file")
    print("3. Check your application - it should work now!")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_status("\nInstallation cancelled by user", "WARNING")
        sys.exit(1)
    except Exception as e:
        print_status(f"Unexpected error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        sys.exit(1)

