# Changelog

All notable changes to DeepFileX will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### 🔄 Planned
- Advanced search filters (regex, date range)
- Dashboard charts (file distribution visualization)
- Multi-language support (English, Japanese)
- AI-based file classification and recommendations

---

## [1.4.1] - 2026-02-09

### 🔧 Fixed
- **Search crash fix**: Resolved application termination during search operations
- **Enhanced exception handling**: Added comprehensive exception handling to `perform_search()` and `display_search_results()` functions
- **Individual result protection**: Improved error handling so single result errors don't cause complete search failure
- **Error logging**: Added detailed traceback logging (`exc_info=True`)
- **User feedback**: Clear error messages and status bar updates on errors

### 📝 Technical Details
- **File**: `src/deepfilex.py:2876-2983`
- **Issue**: PyQt6 signal handlers lacked exception handling
- **Solution**: Comprehensive try-except blocks with logging
- **Impact**: Prevents application crashes during search operations

---

## [1.4.0] - 2026-02-08

### ⬆️ Upgraded
- **PyQt6**: 6.9.1 → 6.10.2
- **PyQt6-WebEngine**: 6.7.0 → 6.10.0
- **PyQt6-Qt6**: 6.9.1 → 6.10.2
- **PyQt6-WebEngine-Qt6**: 6.7.3 → 6.10.2

### 🔧 Fixed
- **DLL loading issue**: Resolved DLL loading failure due to PyQt6 version mismatch
- **UI stability**: Improved web component stability
- **Exception handling**: Added exception handling to various UI event handlers

### 🎨 Improved
- **Performance optimization**: Reduced memory usage and improved response time
- **UI responsiveness**: Enhanced user interface response speed

---

## [1.3.0] - 2026-02-07

### 🎨 Changed
- **Project structure reorganization**
  - Moved source code to `src/` folder
  - Consolidated scripts in `scripts/` folder
  - Organized documentation in `docs/` folder
  - Systematized release files in `releases/` folder
  - Separated build configuration to `build/` folder

### ✨ Added
- **Auto-update system**: Automatic update checker with GitHub API integration
- **`.gitignore`**: Added Python, IDE, and project-specific rules
- **Development guide**: Added contribution guide to README.md
- **CHANGELOG.md**: Version-by-version change documentation

### 🐛 Fixed
- **Unicode/Emoji support**: Full UTF-8 encoding support
- **Logging stability**: Improved logging system error handling

### 🗑️ Removed
- **`__pycache__/`**: Removed cache folder (268KB saved)
- **Empty folders**: Cleaned up unused directories
- **Legacy files**: Archived outdated files

### 🔷 Rebranding
- **Project rename**: Complete rebranding
- **Company branding**: Applied QuantumLayer branding
- **Theme transition**: Changed to professional tech theme
- **Consistency**: Ensured consistency across all files, code, and documentation

---

## [1.2.0] - 2025-08-27

### ✨ Added
- **Installer system**: Everything-style installer complete
- **Installation options**: Custom installation path support

### 🎨 Changed
- **Project structure**: Optimized file structure
- **Build system**: Improved PyInstaller configuration

### 🐛 Fixed
- **Performance improvements**: Optimized scan and search speed
- **File cleanup**: Removed unnecessary files

---

## [1.0.0] - 2025-08-26

### 🎉 Initial Release

#### ✨ Features
- **30+ file format support**
  - Documents: TXT, PDF, DOCX, XLSX, PPTX, HWP
  - Code: PY, JS, JAVA, C, CPP, CS, HTML, CSS
  - Images: JPG, PNG, GIF, BMP, TIFF, WEBP, SVG
  - Archives: ZIP, RAR, 7Z, TAR, GZ

- **SQLite-based indexing**
  - Persistent index storage
  - High-speed search (millisecond response)
  - Index save/load functionality

- **Multi-threaded scanning**
  - Parallel processing for 10,000+ files/min
  - Real-time progress display
  - Memory optimization

- **Modern UI**
  - Light/Dark mode
  - Intuitive user interface
  - PyQt6-based GUI

#### 📦 Deliverables
- DeepFileX.exe (Executable)
- Source code and documentation

---

## Release Links

- **v1.4.1**: [DeepFileX v1.4.1](https://github.com/noblejim/DeepFileX/releases/tag/v1.4.1)
- **v1.4.0**: [DeepFileX v1.4.0](https://github.com/noblejim/DeepFileX/releases/tag/v1.4.0)
- **v1.3.0**: [DeepFileX v1.3.0](https://github.com/noblejim/DeepFileX/releases/tag/v1.3.0)
- **v1.2.0**: [DeepFileX v1.2.0](https://github.com/noblejim/DeepFileX/releases/tag/v1.2.0)
- **v1.0.0**: [DeepFileX v1.0.0](https://github.com/noblejim/DeepFileX/releases/tag/v1.0.0)

---

## Versioning Guide

DeepFileX follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version: Incompatible API changes
- **MINOR** version: Backward-compatible feature additions
- **PATCH** version: Backward-compatible bug fixes

---

**DeepFileX by QuantumLayer** - Advanced File Analysis System 🔷
