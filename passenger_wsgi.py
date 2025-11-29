import sys
import os
import site

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Detect and add virtual environment paths (Namecheap uses virtualenv)
home_dir = os.path.expanduser('~')
python_version = f"{sys.version_info.major}.{sys.version_info.minor}"

# Check for Namecheap virtual environment (common location)
# Note: Some systems use lib64 instead of lib
virtualenv_paths = [
    os.path.join(home_dir, 'virtualenv', 'console', python_version, 'lib64', f'python{python_version}', 'site-packages'),
    os.path.join(home_dir, 'virtualenv', 'console', python_version, 'lib', f'python{python_version}', 'site-packages'),
    os.path.join(home_dir, 'virtualenv', 'console', python_version, 'lib64', 'python3', 'site-packages'),
    os.path.join(home_dir, 'virtualenv', 'console', python_version, 'lib', 'python3', 'site-packages'),
    os.path.join(home_dir, 'virtualenv', 'console', 'lib64', f'python{python_version}', 'site-packages'),
    os.path.join(home_dir, 'virtualenv', 'console', 'lib', f'python{python_version}', 'site-packages'),
]

for venv_path in virtualenv_paths:
    if os.path.exists(venv_path) and venv_path not in sys.path:
        sys.path.insert(0, venv_path)

# Add user site-packages directory (where --user installed packages go)
user_site = site.getusersitepackages()
if user_site and os.path.exists(user_site) and user_site not in sys.path:
    sys.path.insert(0, user_site)

# Also try common user site-packages locations
possible_paths = [
    os.path.join(home_dir, '.local', 'lib', f'python{python_version}', 'site-packages'),
    os.path.join(home_dir, '.local', 'lib', 'python3', 'site-packages'),
]

for path in possible_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)

# Debug: Write paths to file for troubleshooting
try:
    debug_file = os.path.join(os.path.dirname(__file__), 'passenger_debug.log')
    with open(debug_file, 'w') as f:
        f.write(f"Python version: {sys.version}\n")
        f.write(f"Python path:\n")
        for p in sys.path:
            f.write(f"  {p}\n")
        f.write(f"\nVirtualenv paths checked:\n")
        for vp in virtualenv_paths:
            exists = os.path.exists(vp)
            f.write(f"  {vp} - {'EXISTS' if exists else 'NOT FOUND'}\n")
except:
    pass  # Don't fail if we can't write debug file

# Import the FastAPI app
try:
    from main import app
except ImportError as e:
    # If import fails, try to provide helpful error
    error_msg = f"Failed to import main.app: {e}\n"
    error_msg += f"Python path: {sys.path}\n"
    error_msg += f"Virtualenv paths checked: {virtualenv_paths}\n"
    try:
        with open(os.path.join(os.path.dirname(__file__), 'import_error.log'), 'w') as f:
            f.write(error_msg)
    except:
        pass
    raise

# Convert ASGI app to WSGI
# IMPORTANT: Do NOT use mangum - it's for AWS Lambda, not WSGI/Passenger!
# We use asgiref with a proper WSGI wrapper function for Passenger compatibility

try:
    from asgiref.wsgi import WsgiToAsgi
except ImportError:
    raise ImportError(
        "asgiref is required but not installed. "
        "Please install it: pip install asgiref"
    )

# Create WSGI adapter instance
_wsgi_adapter = WsgiToAsgi(app)

# Create a proper WSGI application function
# Passenger expects a callable that takes (environ, start_response)
# This wrapper ensures proper WSGI interface compatibility
def application(environ, start_response):
    """
    WSGI application function for Passenger.
    This properly wraps the ASGI app to work with Passenger WSGI.
    """
    try:
        # Call the WSGI adapter with proper WSGI interface
        return _wsgi_adapter(environ, start_response)
    except Exception as e:
        # Log error for debugging
        try:
            error_log = os.path.join(os.path.dirname(__file__), 'wsgi_error.log')
            with open(error_log, 'a') as f:
                import traceback
                f.write(f"WSGI Error: {e}\n")
                f.write(traceback.format_exc())
                f.write("\n" + "="*50 + "\n")
        except:
            pass
        # Re-raise to let Passenger handle it
        raise