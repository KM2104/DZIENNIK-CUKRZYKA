# -*- mode: python ; coding: utf-8 -*-
"""
Konfiguracja PyInstaller dla Health Monitor
Użyj: pyinstaller HealthMonitor_custom.spec
"""

from kivy_deps import sdl2, glew, angle
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Zbierz wszystkie ukryte importy
hiddenimports = [
    # Kivy podstawowe
    'kivy.core.window.window_info',
    'kivy.core.text',
    'kivy.core.image',
    'kivy.input.providers.mouse',
    # Matplotlib
    'matplotlib.pyplot',
    'matplotlib.backends.backend_agg',
    # ReportLab
    'reportlab.pdfgen.canvas',
    'reportlab.lib.pagesizes',
    'reportlab.pdfbase',
    'reportlab.pdfbase.ttfonts',
    # Garden
    'kivy_garden.graph',
    # Dodatkowe
    'win32timezone',
    'pkg_resources.extern',
]

# Zbierz dane
datas = [
    ('health.kv', '.'),
]

# Zbierz binaria Kivy
binaries = []

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Wyklucz niepotrzebne moduły aby zmniejszyć rozmiar
        'tkinter',
        'test',
        'unittest',
        'email',
        'http',
        'xml',
        'pydoc',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + angle.dep_bins)],
    name='HealthMonitor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Bez konsoli - GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Możesz dodać: icon='icon.ico'
)
