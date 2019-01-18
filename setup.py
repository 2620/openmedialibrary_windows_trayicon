import sys
from cx_Freeze import setup, Executable

'''
to build run: python.exe setup.py bdist_msi
'''

build_exe_options = {
    "packages": ["os"],
    "excludes": ["tkinter"],
    "include_msvcr": True,
    "include_files": [
        "ico",
        "index.html",
        "js",
        "png",
        "svg",
    ]
}

bdist_msi_options = {
    "upgrade_code": "{d2ff6dae-c817-11e5-bedb-08002781ab3d}"
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

oml = Executable(
    "Open Media Library.py", base=base,
    shortcutName="Open Media Library",
    shortcutDir="ProgramMenuFolder",
    icon="ico/oml.ico"
)

setup(
    name="Open Media Library",
    version="0.2",
    description="Open Media Library",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    },
    executables=[oml]
)
