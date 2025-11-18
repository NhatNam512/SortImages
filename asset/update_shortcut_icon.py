"""
Script cập nhật icon cho shortcut đã có trên Windows
Chạy script này để đổi icon cho shortcut đã tạo trước đó
"""

import os
import sys

def update_shortcut_icon():
    """Cập nhật icon cho shortcut đã có"""
    
    try:
        import win32com.client
    except ImportError:
        print("Dang cai dat pywin32...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
        import win32com.client
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Tìm file icon
    icon_path = None
    icon_ico = os.path.join(script_dir, "icon.ico")
    icon_png = os.path.join(script_dir, "icon.png")
    
    if os.path.exists(icon_ico):
        icon_path = icon_ico
    elif os.path.exists(icon_png):
        icon_path = icon_png
    else:
        print("[LOI] Khong tim thay file icon.ico hoac icon.png")
        print("      Chay create_icon.py de tao icon truoc.")
        return
    
    shell = win32com.client.Dispatch("WScript.Shell")
    
    # Tìm và cập nhật shortcut trên Desktop
    desktop = shell.SpecialFolders("Desktop")
    shortcut_path = os.path.join(desktop, "Sao chep anh nang cao.lnk")
    
    if os.path.exists(shortcut_path):
        try:
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.IconLocation = f"{icon_path},0"
            shortcut.save()
            print(f"[OK] Da cap nhat icon cho shortcut tren Desktop")
            print(f"     Icon: {icon_path}")
        except Exception as e:
            print(f"[LOI] Khong the cap nhat shortcut tren Desktop: {e}")
    else:
        print(f"[CHU Y] Khong tim thay shortcut tren Desktop: {shortcut_path}")
        print("        Chay create_shortcut.py de tao shortcut truoc.")
    
    # Tìm và cập nhật shortcut trong Start Menu
    try:
        start_menu = shell.SpecialFolders("StartMenu")
        programs_folder = os.path.join(start_menu, "Programs")
        if not os.path.exists(programs_folder):
            programs_folder = start_menu
        
        shortcut_path2 = os.path.join(programs_folder, "Sao chep anh nang cao.lnk")
        if os.path.exists(shortcut_path2):
            shortcut2 = shell.CreateShortCut(shortcut_path2)
            shortcut2.IconLocation = f"{icon_path},0"
            shortcut2.save()
            print(f"[OK] Da cap nhat icon cho shortcut trong Start Menu")
    except Exception as e:
        pass  # Không bắt buộc phải có shortcut trong Start Menu
    
    print("\n[HOAN THANH] Da cap nhat icon cho shortcut!")

if __name__ == "__main__":
    try:
        update_shortcut_icon()
    except Exception as e:
        print(f"[LOI] Loi khi cap nhat icon: {e}")

