#!/usr/bin/env python3
"""
Installation Verification Script

This script checks if all required dependencies and tools are properly installed.
Run this after installation to verify your setup.
"""

import sys
import subprocess
import importlib


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print("Checking Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} (requires 3.8+)")
        return False


def check_python_package(package_name, import_name=None):
    """Check if a Python package is installed"""
    import_name = import_name or package_name
    print(f"Checking {package_name}...", end=" ")
    try:
        importlib.import_module(import_name)
        print("✓")
        return True
    except ImportError:
        print("✗ Not installed")
        return False


def check_ffmpeg():
    """Check if FFmpeg is installed"""
    print("Checking FFmpeg...", end=" ")
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            check=True
        )
        version_line = result.stdout.decode().split('\n')[0]
        print(f"✓ {version_line}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Not installed")
        return False


def check_env_file():
    """Check if .env file exists"""
    import os
    print("Checking .env file...", end=" ")
    if os.path.exists('.env'):
        print("✓ Found")
        return True
    else:
        print("⚠ Not found (copy .env.template to .env)")
        return False


def check_api_keys():
    """Check if API keys are configured"""
    import os
    from pathlib import Path

    # Try to load .env file
    env_file = Path('.env')
    if not env_file.exists():
        print("API keys: ⚠ .env file not found")
        return False

    with open(env_file) as f:
        content = f.read()

    print("\nChecking API keys:")

    keys_to_check = {
        'HUGGINGFACE_API_KEY': 'Hugging Face (required)',
        'DID_API_KEY': 'D-ID (required)',
        'DEEPMOTION_API_KEY': 'DeepMotion (optional)',
    }

    all_configured = True
    for key, description in keys_to_check.items():
        if key in content and 'your_' not in content.split(key)[1].split('\n')[0]:
            print(f"  {description}: ✓")
        else:
            required = 'required' in description
            symbol = '✗' if required else '⚠'
            print(f"  {description}: {symbol} Not configured")
            if required:
                all_configured = False

    return all_configured


def check_directories():
    """Check if output directories exist or can be created"""
    from pathlib import Path

    print("\nChecking directories:")

    dirs = ['output', 'output/avatars', 'output/animations', 'output/episodes', 'projects']

    for dir_path in dirs:
        p = Path(dir_path)
        if p.exists():
            print(f"  {dir_path}: ✓")
        else:
            try:
                p.mkdir(parents=True, exist_ok=True)
                print(f"  {dir_path}: ✓ Created")
            except Exception as e:
                print(f"  {dir_path}: ✗ Cannot create ({e})")
                return False

    return True


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("Animated Reality Show - Installation Verification")
    print("=" * 60)
    print()

    checks = []

    # Python version
    checks.append(check_python_version())
    print()

    # Python packages
    print("Checking Python packages:")
    packages = [
        ('requests', 'requests'),
        ('Pillow', 'PIL'),
        ('numpy', 'numpy'),
        ('opencv-python', 'cv2'),
        ('huggingface-hub', 'huggingface_hub'),
        ('python-dotenv', 'dotenv'),
    ]

    for package_name, import_name in packages:
        checks.append(check_python_package(package_name, import_name))

    print()

    # FFmpeg
    checks.append(check_ffmpeg())
    print()

    # Configuration files
    checks.append(check_env_file())

    # API keys
    api_keys_ok = check_api_keys()
    # Note: API keys are not strictly required for testing

    # Directories
    print()
    checks.append(check_directories())

    # Summary
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)

    all_passed = all(checks)

    if all_passed:
        print("✓ All core components are properly installed!")
        print()
        if not api_keys_ok:
            print("⚠ Note: API keys are not fully configured.")
            print("  Configure them in .env to use the full functionality.")
        print()
        print("You're ready to create your first episode!")
        print("Try: python Scripts/examples.py")
    else:
        print("✗ Some components are missing or not properly installed.")
        print()
        print("Please fix the issues above and run this script again.")
        print()
        print("For help, see:")
        print("  - QUICKSTART.md")
        print("  - README.md")

    print()
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
