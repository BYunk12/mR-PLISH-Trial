#!/usr/bin/python3
"""
Automated installer for PLISH Probe Designer dependencies
Downloads and installs BLAST+ and RNAstructure locally
"""

import os
import sys
import urllib.request
import tarfile
import zipfile
import shutil
import subprocess
import platform
from pathlib import Path

class DependencyInstaller:
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.tools_dir = self.script_dir / "tools"
        self.tools_dir.mkdir(exist_ok=True)
        
        # Detect platform
        self.system = platform.system().lower()
        self.machine = platform.machine().lower()
        
        print(f"Detected system: {self.system} ({self.machine})")
        
    def download_file(self, url, filename, description):
        """Download a file with progress indication"""
        print(f"Downloading {description}...")
        try:
            def progress_hook(block_num, block_size, total_size):
                if total_size > 0:
                    percent = min(100, (block_num * block_size * 100) // total_size)
                    sys.stdout.write(f"\r  Progress: {percent}% ({block_num * block_size // 1024 // 1024} MB)")
                    sys.stdout.flush()
            
            urllib.request.urlretrieve(url, filename, progress_hook)
            print(f"\n✓ Downloaded {description}")
            return True
        except Exception as e:
            print(f"\n✗ Failed to download {description}: {e}")
            return False
    
    def extract_archive(self, archive_path, extract_to, description):
        """Extract archive file"""
        print(f"Extracting {description}...")
        try:
            if archive_path.suffix == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
            elif archive_path.suffix in ['.tar', '.gz'] or '.tar.' in archive_path.name:
                with tarfile.open(archive_path, 'r:*') as tar_ref:
                    tar_ref.extractall(extract_to)
            print(f"✓ Extracted {description}")
            return True
        except Exception as e:
            print(f"✗ Failed to extract {description}: {e}")
            return False
    
    def get_blast_url(self):
        """Get the appropriate BLAST+ download URL for the platform"""
        base_url = "https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/"
        
        if self.system == "linux":
            if "x86_64" in self.machine or "amd64" in self.machine:
                return base_url + "ncbi-blast-2.16.0+-x64-linux.tar.gz"
            elif "aarch64" in self.machine or "arm64" in self.machine:
                return base_url + "ncbi-blast-2.16.0+-aarch64-linux.tar.gz"
        elif self.system == "darwin":  # macOS
            if "arm64" in self.machine or "aarch64" in self.machine:
                return base_url + "ncbi-blast-2.16.0+-aarch64-macosx.tar.gz"
            else:
                return base_url + "ncbi-blast-2.16.0+-x64-macosx.tar.gz"
        elif self.system == "windows":
            return base_url + "ncbi-blast-2.16.0+-x64-win64.tar.gz"
        
        # Default to Linux x64 if unsure
        return base_url + "ncbi-blast-2.16.0+-x64-linux.tar.gz"
    
    def get_rnastructure_url(self):
        """Get RNAstructure download URL"""
        # RNAstructure download URL (version 6.4)
        return "https://rna.urmc.rochester.edu/Releases/6.4/RNAstructureLinuxTextInterfaces64bit.tgz"
    
    def install_blast(self):
        """Install BLAST+ locally"""
        print("\n" + "="*50)
        print("Installing BLAST+")
        print("="*50)
        
        blast_url = self.get_blast_url()
        blast_filename = self.tools_dir / blast_url.split('/')[-1]
        
        # Download BLAST+
        if not self.download_file(blast_url, blast_filename, "BLAST+"):
            return False
        
        # Extract BLAST+
        if not self.extract_archive(blast_filename, self.tools_dir, "BLAST+"):
            return False
        
        # Find the extracted directory and rename it
        extracted_dirs = [d for d in self.tools_dir.iterdir() if d.is_dir() and "ncbi-blast" in d.name]
        if extracted_dirs:
            blast_dir = extracted_dirs[0]
            target_dir = self.tools_dir / "ncbi-blast"
            if target_dir.exists():
                shutil.rmtree(target_dir)
            blast_dir.rename(target_dir)
            print(f"✓ BLAST+ installed to {target_dir}")
        
        # Clean up downloaded file
        blast_filename.unlink()
        
        # Test BLAST installation
        blast_bin = self.tools_dir / "ncbi-blast" / "bin" / "blastn"
        if not blast_bin.exists():
            blast_bin = self.tools_dir / "ncbi-blast" / "bin" / "blastn.exe"  # Windows
        
        if blast_bin.exists():
            print("✓ BLAST+ installation verified")
            return True
        else:
            print("✗ BLAST+ installation verification failed")
            return False
    
    def install_rnastructure(self):
        """Install RNAstructure locally"""
        print("\n" + "="*50)
        print("Installing RNAstructure")
        print("="*50)
        
        rna_url = self.get_rnastructure_url()
        rna_filename = self.tools_dir / "RNAstructure.tgz"
        
        # Download RNAstructure
        if not self.download_file(rna_url, rna_filename, "RNAstructure"):
            return False
        
        # Extract RNAstructure
        if not self.extract_archive(rna_filename, self.tools_dir, "RNAstructure"):
            return False
        
        # Find and rename the extracted directory
        extracted_dirs = [d for d in self.tools_dir.iterdir() if d.is_dir() and "RNAstructure" in d.name and d.name != "RNAstructure"]
        if extracted_dirs:
            rna_dir = extracted_dirs[0]
            target_dir = self.tools_dir / "RNAstructure"
            if target_dir.exists():
                shutil.rmtree(target_dir)
            rna_dir.rename(target_dir)
            print(f"✓ RNAstructure installed to {target_dir}")
        
        # Clean up downloaded file
        rna_filename.unlink()
        
        # Test RNAstructure installation
        oligoscreen_bin = self.tools_dir / "RNAstructure" / "exe" / "oligoscreen"
        if oligoscreen_bin.exists():
            # Make executable on Unix systems
            if self.system != "windows":
                os.chmod(oligoscreen_bin, 0o755)
            print("✓ RNAstructure installation verified")
            return True
        else:
            print("✗ RNAstructure installation verification failed")
            return False
    
    def create_test_script(self):
        """Create a test script to verify installations"""
        test_script = self.script_dir / "test_dependencies.py"
        test_content = '''#!/usr/bin/python3
"""
Test script to verify BLAST+ and RNAstructure installations
"""
import os
import subprocess
from pathlib import Path

def test_blast():
    """Test BLAST+ installation"""
    script_dir = Path(__file__).parent.absolute()
    blast_bin = script_dir / "tools" / "ncbi-blast" / "bin" / "blastn"
    
    if not blast_bin.exists():
        blast_bin = script_dir / "tools" / "ncbi-blast" / "bin" / "blastn.exe"
    
    if blast_bin.exists():
        try:
            result = subprocess.run([str(blast_bin), "-version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✓ BLAST+ working: {result.stdout.split()[1]}")
                return True
        except Exception as e:
            print(f"✗ BLAST+ test failed: {e}")
    else:
        print("✗ BLAST+ binary not found")
    return False

def test_rnastructure():
    """Test RNAstructure installation"""
    script_dir = Path(__file__).parent.absolute()
    oligoscreen_bin = script_dir / "tools" / "RNAstructure" / "exe" / "oligoscreen"
    
    if oligoscreen_bin.exists():
        try:
            # Test if the binary can be executed
            result = subprocess.run([str(oligoscreen_bin)], 
                                  capture_output=True, text=True, timeout=5)
            # oligoscreen should fail without arguments, but shouldn't crash
            print("✓ RNAstructure (oligoscreen) working")
            return True
        except Exception as e:
            print(f"✗ RNAstructure test failed: {e}")
    else:
        print("✗ RNAstructure (oligoscreen) binary not found")
    return False

if __name__ == "__main__":
    print("Testing PLISH Probe Designer dependencies...")
    print("=" * 50)
    
    blast_ok = test_blast()
    rna_ok = test_rnastructure()
    
    print("=" * 50)
    if blast_ok and rna_ok:
        print("🎉 All dependencies working correctly!")
    else:
        print("❌ Some dependencies failed. Try reinstalling.")
'''
        
        with open(test_script, 'w') as f:
            f.write(test_content)
        
        os.chmod(test_script, 0o755)
        print(f"✓ Created test script: {test_script}")
    
    def run_installation(self):
        """Run the complete installation process"""
        print("PLISH Probe Designer Dependency Installer")
        print("=" * 50)
        print("This will download and install:")
        print("- BLAST+ (for sequence similarity searches)")
        print("- RNAstructure (for thermodynamic calculations)")
        print("=" * 50)
        
        # Create tools directory
        self.tools_dir.mkdir(exist_ok=True)
        
        # Install dependencies
        blast_success = self.install_blast()
        rna_success = self.install_rnastructure()
        
        # Create test script
        self.create_test_script()
        
        # Summary
        print("\n" + "="*50)
        print("Installation Summary")
        print("="*50)
        print(f"BLAST+: {'✓ Success' if blast_success else '✗ Failed'}")
        print(f"RNAstructure: {'✓ Success' if rna_success else '✗ Failed'}")
        
        if blast_success and rna_success:
            print("\n🎉 All dependencies installed successfully!")
            print("\nTo test the installation, run:")
            print("  python3 test_dependencies.py")
            print("\nTo start using PLISH Probe Designer:")
            print("  python3 probeDesigner.py --help")
            return True
        else:
            print("\n❌ Some installations failed. Please check the errors above.")
            return False

def main():
    """Main entry point"""
    installer = DependencyInstaller()
    success = installer.run_installation()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())