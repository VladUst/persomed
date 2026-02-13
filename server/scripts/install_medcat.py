#!/usr/bin/env python
"""
Script to install MedCAT using Python 3.11.8
"""
import subprocess
import sys
import os

# Path to Python 3.11.8
PYTHON_PATH = r"C:\Users\vladu\.pyenv\pyenv-win\versions\3.11.8\python.exe"

def main():
    print("Starting MedCAT installation with Python 3.11.8...")
    
    # Create virtual environment
    venv_path = "venv-medcat"
    if not os.path.exists(venv_path):
        subprocess.run([PYTHON_PATH, "-m", "venv", venv_path], check=True)
    
    # Paths in the virtual environment
    python_venv = os.path.join(venv_path, "Scripts", "python.exe")
    
    # Upgrade pip and setuptools using the venv's Python
    print("Upgrading pip and setuptools...")
    subprocess.run([python_venv, "-m", "pip", "install", "--upgrade", "pip", "setuptools"], check=True)
    
    # Install MedCAT
    print("Installing MedCAT...")
    subprocess.run([python_venv, "-m", "pip", "install", "medcat"], check=True)
    
    print("\nInstallation complete!")
    print(f"\nTo activate the environment, run:")
    print(f"   .\\{venv_path}\\Scripts\\activate")
    print("\nThen you can import medcat in your Python scripts.")

if __name__ == "__main__":
    main() 