# 🔷 DeepFileX

**DeepFileX** - Next-Generation File Search and Analysis Solution

> **Latest**: v1.4.1 (2026-02-09) - Stability improvements and bug fixes

[![Latest Release](https://img.shields.io/github/v/release/noblejim/DeepFileX)](https://github.com/noblejim/DeepFileX/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.txt)

## 🎯 Overview

DeepFileX is an innovative file management tool that analyzes file systems with advanced algorithms. It provides fast and accurate file searching and indexing capabilities.

## 🚀 Quick Start

### Download & Run

1. **[Download Latest Release](https://github.com/noblejim/DeepFileX/releases)**
2. **Run DeepFileX.exe**

For developer mode, see the [Development Guide](#-development-guide).

## ⭐ Core Features

### 🔬 Advanced File Analysis
- **30+ File Format Support**: Documents, code, images, archives
- **Real-time Search**: Search by filename and content
- **Persistent Indexing**: SQLite-based database

### ⚡ Ultra-Fast Performance
- **Multi-threading**: Parallel processing for rapid scanning
- **10,000+ Files/Min**: Handle large directories efficiently
- **Memory Optimized**: Efficient resource usage

### 🎨 Modern UI
- **Light/Dark Mode**: Eye-friendly themes
- **Intuitive Interface**: Easy to use
- **Real-time Progress**: Live operation status

## 📁 Supported File Formats

| Category | Extensions |
|----------|-----------|
| **📄 Documents** | `.txt`, `.md`, `.log`, `.csv`, `.json`, `.xml`, `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.hwp` |
| **💻 Code** | `.py`, `.js`, `.java`, `.c`, `.cpp`, `.cs`, `.html`, `.css`, `.php`, `.go`, `.rs` |
| **🖼️ Images** | `.jpg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.svg`, `.ico` |
| **📦 Archives** | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2` |

## 💾 System Requirements

- **OS**: Windows 10+ (64-bit)
- **RAM**: 4GB+ recommended
- **Storage**: 100MB+
- **Python**: 3.8+ (developer mode only)

## 📊 Performance Metrics

- Scan Speed: **10,000+ files/minute**
- Search Speed: **Millisecond response time**
- Memory Usage: **~100MB**

## 🔧 Usage

### 1️⃣ File Scanning
1. Click "Scan Folders" to select directory
2. Click "Start Scan" to begin scanning
3. View real-time progress

### 2️⃣ File Search
1. Enter keywords in search box
2. Press Enter or click "Search" button
3. Select file from results to preview

### 3️⃣ Index Management
- **Save Index**: Save current index
- **Load Index**: Load saved index
- **Clear Records**: Reset index

## 📈 Recent Updates

### v1.4.1 (2026-02-09)
- 🔧 Fixed search crash issue
- 🛡️ Enhanced exception handling
- 📝 Added detailed error logging

### v1.4.0 (2026-02-08)
- ⬆️ PyQt6 6.10.2 upgrade
- 🐛 UI stability improvements
- 🎨 Performance optimization

### v1.3.0 (2026-02-07)
- 🎨 Project structure reorganization
- ✨ Auto-update system
- 🐛 Unicode/Emoji support improvements

📖 See [CHANGELOG.md](CHANGELOG.md) for complete change history.

## 🛠️ Development Guide

### Setup Development Environment

```bash
# 1. Clone repository
git clone https://github.com/noblejim/DeepFileX.git
cd DeepFileX

# 2. Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python src\deepfilex.py
```

### Building

```bash
# Build executable with PyInstaller
pyinstaller build\specs\DeepFileX_v1.4.1.spec --clean
```

Build output: `build/temp/dist/DeepFileX.exe`

### Project Structure

```
DeepFileX/
├── src/                   # Source code
│   ├── deepfilex.py       # Main application
│   ├── update_checker.py  # Auto-update
│   └── version_config.py  # Version management
├── tests/                 # Test files
├── build/                 # Build configuration
│   ├── specs/             # PyInstaller specs
│   └── scripts/           # Build scripts
├── docs/                  # Documentation
│   ├── releases/          # Release notes
│   └── CONTRIBUTING.md    # Contribution guide
├── README.md              # Project overview
├── CHANGELOG.md           # Change history
├── LICENSE.txt            # MIT License
└── requirements.txt       # Dependencies
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** and clone the repository
2. **Create branch**: `git checkout -b feature/AmazingFeature`
3. **Commit changes**: `git commit -m "✨ feat: Add AmazingFeature"`
4. **Push**: `git push origin feature/AmazingFeature`
5. **Create Pull Request**

### Contribution Guidelines

- ✅ Follow PEP 8 coding style
- ✅ Test changes thoroughly
- ✅ Update documentation for new features
- ✅ Maintain Python 3.8+ compatibility
- ✅ Reference related issue numbers in PRs

## 📝 License

This project is licensed under the MIT License. See [LICENSE.txt](LICENSE.txt) for details.

## 📞 Support & Contact

- **GitHub**: https://github.com/noblejim/DeepFileX
- **Releases**: https://github.com/noblejim/DeepFileX/releases
- **Issues**: https://github.com/noblejim/DeepFileX/issues
- **Discussions**: https://github.com/noblejim/DeepFileX/discussions

---

**DeepFileX v1.4.1** by **QuantumLayer** - Advanced File Analysis System 🔷
