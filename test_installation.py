#!/usr/bin/env python3
# Test Installation Script for Bot Cloudflare Pro
# Created by @bukanaol

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported."""
    try:
        if package_name:
            importlib.import_module(module_name)
            print(f"✅ {package_name} imported successfully")
            return True
        else:
            importlib.import_module(module_name)
            print(f"✅ {module_name} imported successfully")
            return True
    except ImportError as e:
        print(f"❌ Failed to import {package_name or module_name}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Warning importing {package_name or module_name}: {e}")
        return True

def test_python_version():
    """Test Python version compatibility."""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python version is compatible (3.8+)")
        return True
    else:
        print("❌ Python version is too old. Required: 3.8+")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Bot Cloudflare Pro Installation")
    print("👨‍💻 Created by @bukanaol")
    print("=" * 50)
    
    # Test Python version
    python_ok = test_python_version()
    print()
    
    # Test required modules
    print("📦 Testing required modules:")
    required_modules = [
        ("telebot", "pyTelegramBotAPI"),
        ("requests", "requests"),
        ("dotenv", "python-dotenv"),
        ("schedule", "schedule"),
        ("cloudflare", "cloudflare"),
        ("cryptography", "cryptography")
    ]
    
    modules_ok = True
    for module, package in required_modules:
        if not test_import(module, package):
            modules_ok = False
    
    print()
    
    # Test optional modules
    print("🔧 Testing optional modules:")
    optional_modules = [
        ("termcolor", "termcolor"),
        ("colorama", "colorama")
    ]
    
    for module, package in optional_modules:
        test_import(module, package)
    
    print()
    
    # Test local modules
    print("🏠 Testing local modules:")
    local_modules = ["config", "utils"]
    
    local_ok = True
    for module in local_modules:
        if not test_import(module):
            local_ok = False
    
    print()
    
    # Test file existence
    print("📁 Testing file structure:")
    required_files = [
        "botcf.py",
        "requirements.txt",
        "README.md",
        ".env.example"
    ]
    
    files_ok = True
    for file in required_files:
        try:
            with open(file, 'r') as f:
                print(f"✅ {file} exists and readable")
        except FileNotFoundError:
            print(f"❌ {file} not found")
            files_ok = False
        except Exception as e:
            print(f"⚠️  {file} has issues: {e}")
    
    print()
    
    # Summary
    print("=" * 50)
    print("📊 Installation Test Summary:")
    
    if python_ok and modules_ok and local_ok and files_ok:
        print("🎉 All tests passed! Bot is ready to run.")
        print("🚀 Use 'python3 botcf.py' to start the bot.")
        print("📖 Check README.md for detailed instructions.")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        if not python_ok:
            print("💡 Install Python 3.8 or higher")
        if not modules_ok:
            print("💡 Run: pip install -r requirements.txt")
        if not local_ok:
            print("💡 Check if all source files are present")
        if not files_ok:
            print("💡 Verify repository structure")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)