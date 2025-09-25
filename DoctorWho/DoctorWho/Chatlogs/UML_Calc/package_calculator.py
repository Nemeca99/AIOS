"""
UML Calculator V1 - Packaging Script
Prepares the calculator for distribution
"""

import os
import shutil
import sys
import subprocess
import platform

def create_directory_if_not_exists(path):
    """Create a directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)

def copy_files_to_dist(src_dir, dist_dir):
    """Copy project files to the distribution directory"""
    # Copy the core Python files
    print(f"Copying Python files from {src_dir} to {dist_dir}...")
    for root, dirs, files in os.walk(src_dir):
        # Skip __pycache__ directories
        if "__pycache__" in root:
            continue
        
        # Create the corresponding directory structure
        rel_path = os.path.relpath(root, src_dir)
        dest_dir = os.path.join(dist_dir, rel_path) if rel_path != '.' else dist_dir
        create_directory_if_not_exists(dest_dir)
        
        # Copy Python files
        for file in files:
            if file.endswith(".py") or file.endswith(".bat"):
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_dir, file)
                print(f"Copying {src_file} to {dest_file}")
                shutil.copy2(src_file, dest_file)

def create_exe_package(dist_dir):
    """Create an executable package using PyInstaller"""
    try:
        # Check if PyInstaller is installed
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        
        # Build the executable
        script_path = os.path.join(dist_dir, "calculator.py")
        output_path = os.path.join(os.path.dirname(dist_dir), "UML_Calculator_Executable")
        
        # Create PyInstaller command
        pyinstaller_cmd = [
            "pyinstaller",
            "--name=UML_Calculator",
            "--onefile",
            "--windowed",
            "--distpath", output_path,
            script_path
        ]
        
        # Add icon if on Windows
        if platform.system() == "Windows":
            # Uncomment this line if you have an icon file
            # pyinstaller_cmd.extend(["--icon", os.path.join(dist_dir, "icon.ico")])
            pass
        
        # Run PyInstaller
        print("Building executable with PyInstaller...")
        subprocess.run(pyinstaller_cmd, check=True)
        print(f"Executable created in {output_path}")
        
    except Exception as e:
        print(f"Error creating executable: {str(e)}")

def package_calculator(src_dir, dist_dir):
    """Package the calculator for distribution"""
    # Create the distribution directory
    create_directory_if_not_exists(dist_dir)
    
    # Copy project files
    copy_files_to_dist(src_dir, dist_dir)
    
    # Create a file for dependencies
    with open(os.path.join(dist_dir, "requirements.txt"), "w") as f:
        f.write("# UML Calculator V1 Requirements\n")
        f.write("# For building executable\n")
        f.write("pyinstaller\n")
    
    print("\nPackaging complete!")
    print(f"Files prepared in {dist_dir}")
    
    # Ask if the user wants to create an executable
    response = input("\nDo you want to create an executable? (yes/no): ").lower()
    if response in ("yes", "y"):
        create_exe_package(dist_dir)

if __name__ == "__main__":
    # Current directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Distribution directory
    dist_dir = os.path.join(os.path.dirname(current_dir), "UML_Calculator_Dist")
    
    # Package the calculator
    package_calculator(current_dir, dist_dir)
