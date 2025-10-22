from cx_Freeze import setup, Executable
import sys
import os

# Include additional files (like images, music, etc.)
include_files = ['Assets/']

# Base option for GUI (only needed on Windows)
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Bricky",
    version="1.0",
    description="Governo Ladro",
    options={
        "build_exe": {
            "packages": ["pygame"],
            "include_files": include_files,
            "include_msvcr": True,  # for Windows runtime DLLs
            "path": ["Assets/Scripts"] + sys.path,
        }
    },
    executables=[
        Executable(
            "main.py", 
            base=base,
            icon="Assets/Sprites/game_icon.ico",
            target_name="Bricky"
            )
        ]
        
)
