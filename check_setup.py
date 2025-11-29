#!/usr/bin/env python3
"""
Diagnostic script to check if Passenger can find packages
Run this from SSH to see what paths are available
"""

import sys
import os
import site

print("=" * 60)
print("Passenger WSGI Setup Diagnostic")
print("=" * 60)
print()

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print()

print("Current Python path:")
for i, p in enumerate(sys.path, 1):
    print(f"  {i}. {p}")
print()

# Check virtual environment
home_dir = os.path.expanduser('~')
python_version = f"{sys.version_info.major}.{sys.version_info.minor}"

print("Checking virtual environment paths:")
virtualenv_paths = [
    os.path.join(home_dir, 'virtualenv', 'console', python_version, 'lib', f'python{python_version}', 'site-packages'),
    os.path.join(home_dir, 'virtualenv', 'console', python_version, 'lib', 'python3', 'site-packages'),
    os.path.join(home_dir, 'virtualenv', 'console', 'lib', f'python{python_version}', 'site-packages'),
]

for venv_path in virtualenv_paths:
    exists = os.path.exists(venv_path)
    print(f"  {venv_path}")
    print(f"    EXISTS: {exists}")
    if exists:
        # Check if fastapi is there
        fastapi_path = os.path.join(venv_path, 'fastapi')
        print(f"    FastAPI found: {os.path.exists(fastapi_path)}")
        # List some packages
        try:
            packages = [d for d in os.listdir(venv_path) if os.path.isdir(os.path.join(venv_path, d)) and not d.startswith('_')]
            print(f"    Sample packages: {', '.join(packages[:5])}")
        except:
            pass
    print()

# Check user site-packages
user_site = site.getusersitepackages()
print(f"User site-packages: {user_site}")
if user_site:
    print(f"  EXISTS: {os.path.exists(user_site)}")
print()

# Try to import fastapi
print("Testing imports:")
try:
    import fastapi
    print(f"  ✓ fastapi imported successfully from: {fastapi.__file__}")
except ImportError as e:
    print(f"  ✗ fastapi import failed: {e}")

try:
    import asgiref
    print(f"  ✓ asgiref imported successfully from: {asgiref.__file__}")
except ImportError as e:
    print(f"  ✗ asgiref import failed: {e}")

try:
    from asgiref.wsgi import WsgiToAsgi
    print(f"  ✓ WsgiToAsgi imported successfully")
except ImportError as e:
    print(f"  ✗ WsgiToAsgi import failed: {e}")

print()
print("=" * 60)
print("If fastapi import failed, the virtualenv path needs to be added to sys.path")
print("=" * 60)

