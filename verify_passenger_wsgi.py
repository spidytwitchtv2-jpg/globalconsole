#!/usr/bin/env python3
"""
Verification script to check if passenger_wsgi.py is correct
Run this on the server to verify the setup
"""

import os
import sys

print("=" * 60)
print("Passenger WSGI Verification")
print("=" * 60)
print()

wsgi_file = os.path.join(os.path.dirname(__file__), 'passenger_wsgi.py')

if not os.path.exists(wsgi_file):
    print("❌ ERROR: passenger_wsgi.py not found!")
    sys.exit(1)

print(f"Checking: {wsgi_file}")
print()

# Read the file
with open(wsgi_file, 'r') as f:
    content = f.read()

# Check for mangum usage in code (should NOT be present)
# Only flag actual code usage, not comments
lines = content.split('\n')
mangum_in_code = False
mangum_lines = []

for i, line in enumerate(lines, 1):
    stripped = line.strip()
    # Skip comments and docstrings
    if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
        continue
    # Check for actual mangum usage (imports, function calls, etc.)
    if 'from mangum' in stripped.lower() or 'import mangum' in stripped.lower():
        mangum_in_code = True
        mangum_lines.append((i, line.strip()))
    elif 'Mangum(' in stripped or 'mangum.' in stripped.lower():
        mangum_in_code = True
        mangum_lines.append((i, line.strip()))

if mangum_in_code:
    print("❌ ERROR: passenger_wsgi.py contains 'mangum' code usage!")
    print("   Mangum is for AWS Lambda, not Passenger WSGI!")
    print("   You need to upload the updated file.")
    print()
    for line_num, line_content in mangum_lines:
        print(f"   Line {line_num}: {line_content}")
    sys.exit(1)
else:
    print("✓ No mangum code usage found (comments mentioning mangum are OK)")

# Check for asgiref (should be present)
if 'asgiref' in content and 'WsgiToAsgi' in content:
    print("✓ asgiref.wsgi.WsgiToAsgi found (correct)")
else:
    print("❌ ERROR: asgiref.wsgi.WsgiToAsgi not found!")
    print("   The file needs to use asgiref for WSGI conversion.")
    sys.exit(1)

# Check for application variable
if 'application = WsgiToAsgi(app)' in content or 'application = WsgiToAsgi' in content:
    print("✓ WSGI application variable defined correctly")
else:
    print("⚠ WARNING: WSGI application variable might not be defined correctly")

print()
print("=" * 60)
print("File verification complete!")
print("=" * 60)
print()
print("If all checks passed, your passenger_wsgi.py is correct.")
print("If you're still getting mangum errors, try:")
print("1. Delete the old passenger_wsgi.py file completely")
print("2. Upload the new one")
print("3. Clear Python cache: find . -name '*.pyc' -delete")
print("4. Restart Passenger application in cPanel")

