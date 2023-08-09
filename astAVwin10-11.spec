# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_dynamic_libs
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata
from PyInstaller.utils.hooks import collect_all
from kivy_deps import sdl2, glew
import sys
sys.setrecursionlimit(10000)

datas = []
binaries = []

hiddenimports = []

block_cipher = None


a = Analysis(
    ['astAV.py'],
    pathex=[],
    binaries=binaries,
    datas=datas+[('ffmpeg.exe', '.'), ('ffprobe.exe', '.')],
    hiddenimports=hiddenimports,
    hookspath=['hooks'],
    hooksconfig={
        "matplotlib": {
            "backends": "auto",  # auto-detect; the default behavior
            # "backends": "all",  # collect all backends
            # "backends": "TkAgg",  # collect a specific backend
            # "backends": ["TkAgg", "Qt5Agg"],  # collect multiple backends
        },
        "gstreamer": {
            "exclude_plugins": [
                "opencv",
            ],
        },
    },
    runtime_hooks=['add_lib.py'],
    excludes=['*.pyc'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    icon="icons/astAV_logo_color256x256.ico",
    exclude_binaries=False,
    name='astAV',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=['*.dll'],
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,Tree('src', prefix='src', excludes=['*.pyc']),
    Tree('locales', prefix='locales'),
    Tree('icons', prefix='icons'),
    Tree('config', prefix='config', excludes=[]),
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    excludes=['*.pyc'],
    #upx=True,
    #upx_exclude=[],
    name='astAV',
)