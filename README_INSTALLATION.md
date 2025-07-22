# PLISH Probe Designer Installation Guide

## Quick Start (Recommended)

### 1. Automatic Installation
```bash
# Run the automated installer
python3 install_dependencies.py

# Test the installation
python3 test_dependencies.py

# Start using PLISH Probe Designer
python3 probeDesigner.py --help
```

### 2. Interactive Setup
```bash
# Run the interactive setup
python3 setup.py
```

## What Gets Installed

The automated installer downloads and installs:

1. **BLAST+ (latest version)**
   - **Purpose**: Local sequence similarity searches
   - **Size**: ~100-200 MB
   - **Location**: `tools/ncbi-blast/`
   - **Binary**: `tools/ncbi-blast/bin/blastn`

2. **RNAstructure (version 6.4)**
   - **Purpose**: RNA thermodynamic calculations
   - **Size**: ~50-100 MB  
   - **Location**: `tools/RNAstructure/`
   - **Binary**: `tools/RNAstructure/exe/oligoscreen`

## Supported Platforms

- ✅ **Linux x64** (Ubuntu, CentOS, etc.)
- ✅ **Linux ARM64** (Raspberry Pi, etc.)
- ✅ **macOS x64** (Intel Macs)
- ✅ **macOS ARM64** (Apple Silicon M1/M2)
- ✅ **Windows x64**

## Installation Process

1. **Platform Detection**: Automatically detects your operating system and architecture
2. **Download**: Downloads appropriate binaries from official sources
3. **Extraction**: Extracts and organizes files in the correct directory structure
4. **Verification**: Tests that tools work correctly
5. **Cleanup**: Removes downloaded archives

## Manual Installation (If Automatic Fails)

### BLAST+ Manual Installation

1. **Download** from [NCBI FTP](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/):
   ```bash
   # Linux x64
   wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.16.0+-x64-linux.tar.gz
   
   # macOS x64  
   wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.16.0+-x64-macosx.tar.gz
   
   # macOS ARM (M1/M2)
   wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.16.0+-aarch64-macosx.tar.gz
   ```

2. **Extract** to tools directory:
   ```bash
   mkdir -p tools
   tar -xzf ncbi-blast-*.tar.gz -C tools/
   mv tools/ncbi-blast-* tools/ncbi-blast
   ```

### RNAstructure Manual Installation

1. **Download** from [RNAstructure website](https://rna.urmc.rochester.edu/Releases/6.4/):
   ```bash
   wget https://rna.urmc.rochester.edu/Releases/6.4/RNAstructureLinuxTextInterfaces64bit.tgz
   ```

2. **Extract** to tools directory:
   ```bash
   tar -xzf RNAstructureLinuxTextInterfaces64bit.tgz -C tools/
   mv tools/RNAstructure* tools/RNAstructure
   ```

## Directory Structure

After installation, your directory should look like:

```
PLISH-ProbeDesigner/
├── probeDesigner.py
├── createDatabase.py
├── setup.py
├── install_dependencies.py
├── test_dependencies.py
├── tools/
│   ├── ncbi-blast/
│   │   ├── bin/
│   │   │   ├── blastn          # Main BLAST executable
│   │   │   ├── makeblastdb     # Database creation
│   │   │   └── ...
│   │   └── ...
│   └── RNAstructure/
│       ├── exe/
│       │   ├── oligoscreen     # Main RNAstructure tool
│       │   └── ...
│       ├── data_tables/        # Thermodynamic data
│       └── ...
├── src/
│   ├── plishMain.py
│   ├── plishUtils.py
│   └── ...
└── database/                   # Created when you make databases
    └── ...
```

## Troubleshooting

### Permission Issues
```bash
# Make executables runnable
chmod +x tools/ncbi-blast/bin/blastn
chmod +x tools/RNAstructure/exe/oligoscreen
```

### Download Issues
- Check internet connection
- Try manual installation
- Use different mirror sites

### Platform Issues
- Verify your platform with: `python3 -c "import platform; print(platform.system(), platform.machine())"`
- For unsupported platforms, try the Linux x64 version

### Testing Installation
```bash
# Test BLAST+
tools/ncbi-blast/bin/blastn -version

# Test RNAstructure  
tools/RNAstructure/exe/oligoscreen

# Test full integration
python3 test_dependencies.py
```

## Size Requirements

- **Disk Space**: ~300-500 MB for tools
- **Memory**: 1-2 GB RAM recommended for processing
- **Network**: ~300 MB download (one-time)

## Network Security

All downloads are from official sources:
- **BLAST+**: NCBI FTP server (ftp.ncbi.nlm.nih.gov)
- **RNAstructure**: University of Rochester (rna.urmc.rochester.edu)

## Next Steps

After successful installation:

1. **Create a database**: Follow the Database Creation section in README.md
2. **Design probes**: Use the GUI (`python3 probeDesigner.py`) or command line
3. **Optimize performance**: The tools are now ready for the optimization improvements!

## Getting Help

If you encounter issues:
1. Check this troubleshooting section
2. Run `python3 test_dependencies.py` for diagnostics
3. Try manual installation
4. Open an issue with your platform details and error messages