#!/usr/bin/env python3
"""
Build script for foamify package.
"""

import subprocess
import sys
import os
import shutil

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✓ Success!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def clean_build():
    """Clean previous build artifacts."""
    print("\nCleaning previous build artifacts...")
    dirs_to_clean = ["dist", "build", "*.egg-info"]
    
    for dir_pattern in dirs_to_clean:
        try:
            if "*" in dir_pattern:
                import glob
                for path in glob.glob(dir_pattern):
                    if os.path.exists(path):
                        shutil.rmtree(path)
                        print(f"✓ Removed {path}")
            else:
                if os.path.exists(dir_pattern):
                    shutil.rmtree(dir_pattern)
                    print(f"✓ Removed {dir_pattern}")
        except Exception as e:
            print(f"⚠ Warning: Could not remove {dir_pattern}: {e}")

def install_build_tools():
    """Install required build tools."""
    return run_command(
        "venv/Scripts/pip.exe install build twine",
        "Installing build tools"
    )

def build_package():
    """Build the package."""
    return run_command(
        "venv/Scripts/python.exe setup.py sdist bdist_wheel",
        "Building package"
    )

def check_package():
    """Check the package with twine."""
    return run_command(
        "venv/Scripts/python.exe -m twine check dist/*",
        "Checking package"
    )

def main():
    """Main build process."""
    print("🚀 Building foamify package...")
    
    # Clean previous builds
    clean_build()
    
    # Install build tools
    if not install_build_tools():
        print("Failed to install build tools")
        return 1
    
    # Build package
    if not build_package():
        print("Failed to build package")
        return 1
    
    # Check package
    if not check_package():
        print("Package validation failed")
        return 1
    
    print("\n🎉 Package built successfully!")
    print("📦 Files created in dist/ directory")
    print("✅ Package is ready for upload to PyPI")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 