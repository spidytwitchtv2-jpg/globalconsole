"""
Test script to verify the refactored code structure.
This checks the main.py file for correct structure without running it.
"""

def check_main_py():
    """Check if main.py has the correct structure"""
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        "Message model exists": "class Message(Base):" in content,
        "POST endpoint exists": '@app.post("/api/console-data")' in content,
        "GET endpoint exists": '@app.get("/api/console-data"' in content,
        "No login endpoint": '@app.post("/api/login")' not in content,
        "No refresh token endpoint": '@app.get("/api/refresh-token")' not in content,
        "No external API calls": 'https://v2.mnitnetwork.com' not in content,
        "Database helper function": 'def get_messages_from_db' in content,
        "Process incoming data function": 'def process_incoming_data' in content,
        "ConsoleDataPayload model": 'class ConsoleDataPayload' in content,
        "Color mapping preserved": 'color_mapping = {}' in content,
        "get_color_for_app preserved": 'def get_color_for_app' in content,
    }
    
    print("=" * 60)
    print("REFACTORING VERIFICATION")
    print("=" * 60)
    
    all_passed = True
    for check_name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check_name}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("✓ All checks passed! Refactoring successful.")
    else:
        print("✗ Some checks failed. Please review the code.")
    print("=" * 60)
    
    return all_passed

def check_frontend():
    """Check if frontend has been updated correctly"""
    with open('static/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        "No login call": "'/api/login'" not in content,
        "No refresh token call": "'/api/refresh-token'" not in content,
        "Console data fetch exists": "'/api/console-data'" in content,
        "Rendering logic preserved": "function renderConsoleData" in content,
        "Color logic preserved": "appColor" in content,
        "Auto-refresh preserved": "startAutoRefresh" in content,
    }
    
    print("\nFRONTEND VERIFICATION")
    print("=" * 60)
    
    all_passed = True
    for check_name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check_name}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("✓ Frontend checks passed!")
    else:
        print("✗ Some frontend checks failed.")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    backend_ok = check_main_py()
    frontend_ok = check_frontend()
    
    if backend_ok and frontend_ok:
        print("\n🎉 REFACTORING COMPLETE AND VERIFIED!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Start the server: python main.py")
        print("3. Post sample data: python post_data_example.py")
        print("4. View in browser: http://localhost:8002")
    else:
        print("\n⚠️  Please fix the issues above before proceeding.")
