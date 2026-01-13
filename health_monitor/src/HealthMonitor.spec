# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('health.kv', '.')]
binaries = []
hiddenimports = ['kivy.core.window.window_info', 'kivy.core.text', 'kivy.core.image', 'kivy.core.camera', 'kivy.core.spelling', 'kivy.core.audio', 'kivy.core.video', 'kivy.input.providers.mouse', 'kivy.uix.screenmanager', 'kivy.uix.scrollview', 'kivy.uix.popup', 'kivy.garden.graph', 'matplotlib.pyplot', 'matplotlib.backends.backend_agg', 'reportlab.pdfgen.canvas', 'reportlab.lib.pagesizes', 'pkg_resources.py2_warn', 'pkg_resources.markers']
tmp_ret = collect_all('kivy')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('kivy_garden')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='HealthMonitor',
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
    icon='NONE',
)
