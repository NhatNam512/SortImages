"""
Các hàm tiện ích cho ứng dụng
"""

import os
from tkinter import PhotoImage, Tk
from config import ICON_PATHS


def set_window_icon(window: Tk) -> bool:
    """
    Thiết lập icon cho cửa sổ ứng dụng
    
    Args:
        window: Đối tượng Tk window
        
    Returns:
        bool: True nếu đặt icon thành công, False nếu không
    """
    for icon_path in ICON_PATHS:
        if os.path.exists(icon_path):
            try:
                if icon_path.endswith('.ico'):
                    window.iconbitmap(icon_path)
                else:
                    # Sử dụng iconphoto cho PNG và các format khác
                    icon_image = PhotoImage(file=icon_path)
                    window.iconphoto(False, icon_image)
                return True
            except Exception as e:
                print(f"Không thể load icon từ {icon_path}: {e}")
    return False

