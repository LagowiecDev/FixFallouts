from tkinter import Tk, filedialog
import subprocess
import os
import sys
import shutil

root = Tk()
root.withdraw()

filePath = filedialog.askopenfilename(
    title="Select Fallout Launcher",
    filetypes=[
        ("Fallout 3", "FalloutLauncher.exe"),
        ("Fallout New Vegas", "FalloutNVLauncher.exe")
    ]
)

if not filePath:
    sys.exit(0)

filename = os.path.basename(filePath)
game_dir = os.path.dirname(filePath)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(SCRIPT_DIR, "TEMPORARY")
os.makedirs(TEMP_DIR, exist_ok=True)

if filename == "FalloutLauncher.exe":  # Fallout 3
    reg_file_name = "fix_f3.reg"
elif filename == "FalloutNVLauncher.exe":  # Fallout NV
    reg_file_name = "fix_fnv.reg"
else:
    print("Unknown launcher")
    sys.exit(1)

reg_path = os.path.join(TEMP_DIR, reg_file_name)

if os.name == "nt":  # Windows
    installed_path = game_dir.replace("/", "\\")
else:  # Linux/macOS → Wine uses Z:\
    installed_path = r"Z:\\" + game_dir.replace("/", "\\").lstrip("/")

installed_path = installed_path.replace("\\", "\\\\")

if filename == "FalloutLauncher.exe":
    reg_content = f"""REGEDIT4

[HKEY_LOCAL_MACHINE\\Software\\Bethesda Softworks\\Fallout3]
"Installed Path"="{installed_path}"

[HKEY_LOCAL_MACHINE\\Software\\WOW6432Node\\Bethesda Softworks\\Fallout3]
"Installed Path"="{installed_path}"
"""
else:
    reg_content = f"""REGEDIT4

[HKEY_LOCAL_MACHINE\\Software\\Bethesda Softworks\\FalloutNV]
"Installed Path"="{installed_path}"

[HKEY_LOCAL_MACHINE\\Software\\WOW6432Node\\Bethesda Softworks\\FalloutNV]
"Installed Path"="{installed_path}"
"""

with open(reg_path, "w", encoding="utf-8") as f:
    f.write(reg_content)
try:
    if os.name == "nt":
        subprocess.run(["regedit", "/c", reg_path], check=True)
    else:
        subprocess.run(
        ["wine", "regedit", "/c", reg_path],
        check=True,
        env={**dict(os.environ), "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"}
    )
finally:
    shutil.rmtree(TEMP_DIR, ignore_errors=True)

print(f"{filename} registry updated successfully.")