"""
Script build ứng dụng thành file .exe
"""

import PyInstaller.__main__
import os

# Các file cần include
files_to_include = [
    "config.py",
    "utils.py",
    "api_client.py",
    "login_screen.py",
    "main_app.py",
    "icon_loader.py",
    "auth_storage.py",
    "machine_id.py",
]

# Assets
datas = []
if os.path.exists("asset/icon.ico"):
    datas.append(("asset/icon.ico", "asset"))
if os.path.exists("asset/icon.png"):
    datas.append(("asset/icon.png", "asset"))

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--name=AutoFindPhoto',
    '--icon=asset/icon.ico' if os.path.exists("asset/icon.ico") else '',
    '--add-data=asset;asset' if datas else '',
    '--hidden-import=requests',
    '--hidden-import=urllib3',
    '--hidden-import=certifi',
    '--hidden-import=charset_normalizer',
    '--hidden-import=idna',
    '--hidden-import=json',
    '--hidden-import=hashlib',
    '--hidden-import=platform',
    '--hidden-import=subprocess',
    '--hidden-import=uuid',
    '--clean',
])

