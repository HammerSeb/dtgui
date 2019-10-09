
# Pyinstaller spec file is used to build dtgui binaries
#
# Inspired by the iris-ued spec file available here:
#   https://github.com/LaurentRDC/iris-ued

import os, sys

# your cwd should be in the same dir as this file, so .. is the project directory:
basepath = os.path.realpath('..')
builddir = os.path.realpath('.')

a = Analysis([os.path.join(basepath, 'pyi_main.py'), ],
             pathex=[basepath, ],
             binaries=[],
             datas=[],
             hiddenimports=["dask",  # force hook-dask.py
                            "pywt",  # force hook-pywt.py
                            "skued", # force hook-skued.py
                            ],
             hookspath=[builddir],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='dtgui',
          debug=True,
          strip=False,
          upx=False,
          console=True,
          icon=None)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='dtgui')