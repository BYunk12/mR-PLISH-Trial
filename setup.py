#!/usr/bin/python3
"""
Simple setup script for PLISH Probe Designer
Provides multiple installation options for dependencies
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if dependencies are already installed"""
    script_dir = Path(__file__).parent.absolute()
    tools_dir = script_dir / "tools"
    
    blast_ok = False
    rna_ok = False
    
    # Check BLAST+
    blast_bin = tools_dir / "ncbi-blast" / "bin" / "blastn"
    if not blast_bin.exists():
        blast_bin = tools_dir / "ncbi-blast" / "bin" / "blastn.exe"
    
    if blast_bin.exists():
        try:
            result = subprocess.run([str(blast_bin), "-version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                blast_ok = True
        except:
            pass
    
    # Check RNAstructure
    rna_bin = tools_dir / "RNAstructure" / "exe" / "oligoscreen"
    if rna_bin.exists():
        rna_ok = True
    
    return blast_ok, rna_ok

def main():
    """Main setup interface"""
    print("PLISH Probe Designer Setup")
    print("=" * 40)
    
    # Check current status
    blast_ok, rna_ok = check_dependencies()
    
    print("Current Status:")
    print(f"  BLAST+: {'✓ Installed' if blast_ok else '✗ Missing'}")
    print(f"  RNAstructure: {'✓ Installed' if rna_ok else '✗ Missing'}")
    print()
    
    if blast_ok and rna_ok:
        print("🎉 All dependencies are already installed!")
        print("\nYou can now use PLISH Probe Designer:")
        print("  python3 probeDesigner.py --help")
        return 0
    
    print("Setup Options:")
    print("1. Auto-install dependencies (recommended)")
    print("2. Manual installation instructions")
    print("3. Check system packages")
    print("4. Exit")
    
    try:
        choice = input("\nSelect option (1-4): ").strip()
    except KeyboardInterrupt:
        print("\nExiting...")
        return 1
    
    if choice == "1":
        print("\nStarting automatic installation...")
        try:
            result = subprocess.run([sys.executable, "install_dependencies.py"], 
                                  cwd=Path(__file__).parent)
            return result.returncode
        except Exception as e:
            print(f"Error running installer: {e}")
            return 1
    
    elif choice == "2":
        show_manual_instructions()
        return 0
    
    elif choice == "3":
        check_system_packages()
        return 0
    
    elif choice == "4":
        print("Exiting...")
        return 0
    
    else:
        print("Invalid option. Please try again.")
        return main()

def show_manual_instructions():
    """Show manual installation instructions"""
    print("\nManual Installation Instructions")
    print("=" * 40)
    
    print("\n1. BLAST+ Installation:")
    print("   Download from: https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/")
    print("   Choose the appropriate version for your system:")
    print("   - Linux x64: ncbi-blast-2.16.0+-x64-linux.tar.gz")
    print("   - macOS x64: ncbi-blast-2.16.0+-x64-macosx.tar.gz")
    print("   - macOS ARM: ncbi-blast-2.16.0+-aarch64-macosx.tar.gz")
    print("   - Windows: ncbi-blast-2.16.0+-x64-win64.tar.gz")
    print("   Extract to: tools/ncbi-blast/")
    
    print("\n2. RNAstructure Installation:")
    print("   Download from: https://rna.urmc.rochester.edu/Releases/6.4/")
    print("   File: RNAstructureLinuxTextInterfaces64bit.tgz")
    print("   Extract to: tools/RNAstructure/")
    
    print("\n3. Directory Structure:")
    print("   PLISH-ProbeDesigner/")
    print("   ├── tools/")
    print("   │   ├── ncbi-blast/")
    print("   │   │   └── bin/")
    print("   │   │       └── blastn")
    print("   │   └── RNAstructure/")
    print("   │       └── exe/")
    print("   │           └── oligoscreen")
    print("   └── ...")
    
    print("\n4. Test Installation:")
    print("   Run: python3 test_dependencies.py")

def check_system_packages():
    """Check for system-installed packages"""
    print("\nChecking System Packages")
    print("=" * 40)
    
    # Check for BLAST+ in system PATH
    try:
        result = subprocess.run(["blastn", "-version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✓ System BLAST+ found: {result.stdout.split()[1]}")
            print("  Note: PLISH Probe Designer needs local installation in tools/")
        else:
            print("✗ System BLAST+ not found")
    except:
        print("✗ System BLAST+ not found")
    
    # Check for common package managers
    package_managers = [
        ("apt", "sudo apt install ncbi-blast+"),
        ("yum", "sudo yum install ncbi-blast+"),
        ("dnf", "sudo dnf install ncbi-blast+"),
        ("brew", "brew install blast"),
        ("conda", "conda install -c bioconda blast"),
    ]
    
    print("\nPackage Manager Options:")
    for pm, cmd in package_managers:
        try:
            subprocess.run([pm, "--version"], capture_output=True, timeout=5)
            print(f"  ✓ {pm}: {cmd}")
        except:
            pass
    
    print("\nNote: Even if installed system-wide, PLISH Probe Designer")
    print("      expects tools in the local tools/ directory.")

if __name__ == "__main__":
    sys.exit(main())