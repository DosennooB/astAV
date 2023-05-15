# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_dynamic_libs
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata
from PyInstaller.utils.hooks import collect_all
from kivy_deps import sdl2, glew

datas = []
binaries = []

block_cipher = None


a = Analysis(
    ['astAV.py'],
    pathex=[],
    binaries=binaries,
    datas=datas+[('src/gui/main/hauptscreen.kv', 'src/gui/main/'), ('src/gui/main/tasktable.kv', 'src/gui/main/'),
                ('src/gui/task/taskscreen.kv', 'src/gui/task/'), ('src/gui/utils/parambox.kv', 'src/gui/utils/'),
                ('src/gui/render/rendersreen.kv', 'src/gui/render/'),
                ('src/gui/render/rendertask.kv', 'src/gui/render/'),
                ('ffmpeg.exe', '.'), ('ffprobe.exe', '.')],
    hiddenimports=[],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='astAV',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,Tree('src'),
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='astAV',
)
