# Namecheap Deployment Guide

Complete guide for deploying the Console App on Namecheap shared hosting with Passenger WSGI.

## Prerequisites

- Namecheap shared hosting account with Passenger WSGI enabled
- SSH access (recommended) or cPanel File Manager
- Python 3.7+ (Python 3.8+ recommended)

## Quick Start

1. **Upload files** to `/home/yourusername/console/` (or your application directory)
2. **Install packages** using one of the methods below
3. **Configure Passenger** in cPanel (usually auto-detected)
4. **Restart application** in cPanel

## Installation Methods

### Method 1: Web-Based Installation (Easiest - No SSH Required)

1. **Upload `install_web.py`** to your application directory
2. **In cPanel File Manager:**
   - Navigate to your application directory
   - Right-click `install_web.py` → Select "Execute" or "Run"
   - Wait for installation (5-10 minutes)
3. **Or access via browser:**
   ```
   https://yourdomain.com/console/install_web.py
   ```
4. **Restart Passenger application** in cPanel

### Method 2: Python Script Installation (SSH)

```bash
# Navigate to your application directory
cd /home/yourusername/console

# Run the Python installer
python3 install_packages.py
```

### Method 3: Shell Script Installation (SSH)

```bash
# Navigate to your application directory
cd /home/yourusername/console

# Make script executable
chmod +x install.sh

# Run installation
./install.sh
```

### Method 4: Manual Installation (SSH)

```bash
# Navigate to your application directory
cd /home/yourusername/console

# Check Python version
python3 --version

# For Python 3.8+ (most common)
pip3 install --user -r requirements.txt

# For Python 3.7
pip3 install --user -r requirements-py37.txt
```

## Passenger Configuration

### Automatic Configuration

Passenger usually auto-detects your application. Ensure:
- `passenger_wsgi.py` is in your application root
- Application entry point is set to: `application`
- Startup file is: `passenger_wsgi.py`

### Manual Configuration (if needed)

In cPanel **Passenger Applications**:
- **Application root:** `/home/yourusername/console`
- **Application URL:** `console` (or your preferred path)
- **Application startup file:** `passenger_wsgi.py`
- **Application Entry point:** `application`

### .htaccess Configuration (if needed)

If Passenger isn't auto-detected, create `.htaccess`:

```apache
PassengerEnabled On
PassengerAppRoot /home/yourusername/console
PassengerPython /usr/bin/python3
PassengerAppType wsgi
PassengerStartupFile passenger_wsgi.py
```

## Important Notes

### Python Version Compatibility

- **Python 3.8+**: Use `requirements.txt`
- **Python 3.7**: Use `requirements-py37.txt`
- The installation scripts auto-detect your Python version

### Virtual Environment

Namecheap uses virtual environments. The `passenger_wsgi.py` file automatically detects and uses:
- `/home/yourusername/virtualenv/console/3.12/lib/python3.12/site-packages`
- Or similar paths based on your Python version

### WSGI Compatibility

FastAPI is an ASGI framework, but Passenger requires WSGI. The `passenger_wsgi.py` file uses `asgiref.wsgi.WsgiToAsgi` to convert ASGI to WSGI automatically.

**Important:** Do NOT use `mangum` - it's for AWS Lambda, not Passenger WSGI!

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
1. Verify packages are installed: `python3 -c "import fastapi; print('OK')"`
2. Check virtual environment path is correct in `passenger_wsgi.py`
3. Restart Passenger application
4. Clear Python cache: `find . -name "*.pyc" -delete`

### Error: "Could not open requirements file"

**Solution:**
- Make sure you're in the correct directory: `pwd`
- Verify `requirements.txt` exists: `ls -la requirements.txt`
- Navigate to correct directory: `cd /home/yourusername/console`

### Error: "Permission denied"

**Solution:**
- Use `--user` flag: `pip3 install --user -r requirements.txt`
- Or contact hosting support

### Error: "pip not found"

**Solution:**
- Try `pip3` instead of `pip`
- Or use: `python3 -m pip install --user -r requirements.txt`

### Error: "WSGI adapter error" or "Lambda function" error

**Solution:**
- Ensure `passenger_wsgi.py` uses `asgiref.wsgi.WsgiToAsgi` (NOT mangum)
- Delete old `passenger_wsgi.py` and upload the new one
- Uninstall mangum if installed: `pip uninstall mangum -y`
- Clear Python cache and restart

### Packages Installed But Still Getting Errors

1. **Restart Passenger application** in cPanel
2. **Clear Python cache:**
   ```bash
   find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null
   find . -name "*.pyc" -delete
   ```
3. **Check debug logs:**
   - `passenger_debug.log` - Shows paths being used
   - `import_error.log` - Shows import errors if any

### Verify Installation

```bash
# Check if FastAPI is installed
python3 -c "import fastapi; print('FastAPI installed!')"

# Check installed packages
pip3 list | grep fastapi

# Verify passenger_wsgi.py is correct
python3 verify_passenger_wsgi.py
```

## File Permissions

Ensure correct file permissions:

```bash
chmod 644 *.py
chmod 755 .
chmod 644 requirements.txt
```

## Restarting Application

After making changes:

1. **Via cPanel:** Passenger Applications → Restart
2. **Via SSH:**
   ```bash
   touch tmp/restart.txt
   ```

## Security Notes

- After installation, consider removing or protecting `install_web.py`
- Keep `passenger_wsgi.py` up to date
- Don't commit sensitive credentials to version control

## Getting Help

If you encounter issues:

1. Check the debug logs (`passenger_debug.log`, `import_error.log`)
2. Verify Python version matches requirements file
3. Ensure all files are uploaded correctly
4. Check Passenger application logs in cPanel
5. Contact Namecheap support if needed

