"""
Script tạo shortcut (lối tắt) cho ứng dụng trên Windows
Chạy script này để tạo file shortcut trên Desktop và Start Menu
Tự động fallback sang PowerShell nếu pywin32 không hoạt động
"""

import os
import sys
import subprocess

def create_shortcut_powershell():
    """Tạo shortcut bằng PowerShell (fallback method)"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ps_script = os.path.join(script_dir, "create_shortcut_ps.ps1")
    
    if os.path.exists(ps_script):
        print("[INFO] Su dung PowerShell de tao shortcut...")
        try:
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_script],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            print(result.stdout)
            if result.returncode == 0:
                return True
        except Exception as e:
            print(f"[LOI] PowerShell error: {e}")
    return False

def create_shortcut():
    """Tạo shortcut cho ứng dụng"""
    
    # Đường dẫn đến file main.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_py = os.path.join(script_dir, "main.py")
    python_exe = sys.executable
    
    # Đường dẫn icon (ưu tiên .ico cho Windows)
    icon_path = None
    icon_ico = os.path.join(script_dir, "icon.ico")
    icon_png = os.path.join(script_dir, "icon.png")
    
    if os.path.exists(icon_ico):
        icon_path = icon_ico
        print(f"[INFO] Su dung icon: {icon_ico}")
    elif os.path.exists(icon_png):
        icon_path = icon_png
        print(f"[INFO] Su dung icon: {icon_png}")
    else:
        print("[CHU Y] Khong tim thay file icon.ico hoac icon.png")
        print("        Chay create_icon.py de tao icon truoc.")
    
    # Thử dùng pywin32 trước
    try:
        import win32com.client
        use_powershell = False
    except ImportError:
        print("[INFO] pywin32 chua co, thu cai dat...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            import win32com.client
            use_powershell = False
        except:
            print("[CHU Y] Khong the su dung pywin32, chuyen sang PowerShell...")
            use_powershell = True
    
    # Nếu pywin32 không hoạt động, dùng PowerShell
    if use_powershell:
        if create_shortcut_powershell():
            return
        else:
            print("[LOI] Khong the tao shortcut bang PowerShell")
            return
    
    # Dùng pywin32
    try:
        # Tạo shortcut shell
        shell = win32com.client.Dispatch("WScript.Shell")
        
        # Tạo shortcut trên Desktop
        desktop = shell.SpecialFolders("Desktop")
        shortcut_path = os.path.join(desktop, "Sao chep anh nang cao.lnk")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = python_exe
        shortcut.Arguments = f'"{main_py}"'
        shortcut.WorkingDirectory = script_dir
        shortcut.Description = "Ung dung sao chep anh nang cao"
        if icon_path:
            # IconLocation cần format: "path,index" (index thường là 0)
            shortcut.IconLocation = f"{icon_path},0"
            print(f"[OK] Da gan icon cho shortcut: {icon_path}")
        shortcut.save()
        print(f"[OK] Da tao shortcut tren Desktop: {shortcut_path}")
        
        # Tạo shortcut trong thư mục Start Menu (tùy chọn)
        try:
            start_menu = shell.SpecialFolders("StartMenu")
            programs_folder = os.path.join(start_menu, "Programs")
            if not os.path.exists(programs_folder):
                programs_folder = start_menu
            
            shortcut_path2 = os.path.join(programs_folder, "Sao chep anh nang cao.lnk")
            shortcut2 = shell.CreateShortCut(shortcut_path2)
            shortcut2.Targetpath = python_exe
            shortcut2.Arguments = f'"{main_py}"'
            shortcut2.WorkingDirectory = script_dir
            shortcut2.Description = "Ung dung sao chep anh nang cao"
            if icon_path:
                shortcut2.IconLocation = f"{icon_path},0"
            shortcut2.save()
            print(f"[OK] Da tao shortcut trong Start Menu: {shortcut_path2}")
        except Exception as e:
            print(f"[CHU Y] Khong the tao shortcut trong Start Menu: {e}")
        
        print("\n[HOAN THANH] Shortcut da duoc tao!")
        print("Ban co the tim thay shortcut tren Desktop.")
        
    except Exception as e:
        print(f"[LOI] Loi khi su dung pywin32: {e}")
        print("[INFO] Chuyen sang su dung PowerShell...")
        if not create_shortcut_powershell():
            print("[LOI] Khong the tao shortcut bang ca hai phuong phap")
            raise

if __name__ == "__main__":
    try:
        create_shortcut()
    except Exception as e:
        print(f"[LOI] Loi khi tao shortcut: {e}")
        print("\nHay thu chay lai script hoac kiem tra quyen truy cap.")

