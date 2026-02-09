# -*- mode: python ; coding: utf-8 -*-
# DeepFileX v1.4.1 PyInstaller Specification File
# Search Crash Bug Fix Release

block_cipher = None

a = Analysis(
    ['src\\filemri.py'],
    pathex=['C:\\QuantumLayer\\DeepFileX'],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('docs', 'docs'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtWebEngineWidgets',
        'PyQt6.QtWebEngineCore',
        'sqlite3',
        'chardet',
        'PyPDF2',
        'docx',
        'openpyxl',
        'pptx',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'torch',
        'pandas',
        'scipy',
        'sklearn',
        'tensorflow',
        'matplotlib',
        'numpy',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DeepFileX',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path if available
    version_file=None,  # Add version info if available
)
