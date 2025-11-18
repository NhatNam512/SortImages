"""
Module tải và quản lý icon cho ứng dụng
"""

import os
from tkinter import PhotoImage, Label

# Đường dẫn thư mục icon
ICON_DIR = "asset"
ICONS_DIR = os.path.join(ICON_DIR, "icons")

# Mapping icon names
ICON_MAP = {
    "app": "app_icon.png",
    "search": "search.png",
    "user": "user.png",
    "password": "lock.png",
    "email": "email.png",
    "invite": "star.png",
    "eye": "eye.png",
    "eye_slash": "eye_slash.png",
}


def load_icon(icon_name: str, size: tuple = (24, 24)) -> PhotoImage:
    """
    Tải icon từ file hoặc trả về None nếu không tìm thấy
    
    Args:
        icon_name: Tên icon (app, search, user, password, email, invite, eye, eye_slash)
        size: Kích thước icon (width, height)
        
    Returns:
        PhotoImage object hoặc None
    """
    if icon_name not in ICON_MAP:
        return None
    
    icon_file = ICON_MAP[icon_name]
    icon_path = os.path.join(ICONS_DIR, icon_file)
    
    # Nếu không có thư mục icons, thử tìm trong asset
    if not os.path.exists(icon_path):
        icon_path = os.path.join(ICON_DIR, icon_file)
    
    if os.path.exists(icon_path):
        try:
            img = PhotoImage(file=icon_path)
            # Resize nếu cần
            if size != (img.width(), img.height()):
                # Tkinter PhotoImage không hỗ trợ resize trực tiếp, cần PIL
                try:
                    from PIL import Image, ImageTk
                    pil_img = Image.open(icon_path)
                    pil_img = pil_img.resize(size, Image.Resampling.LANCZOS)
                    img = ImageTk.PhotoImage(pil_img)
                except ImportError:
                    pass  # Nếu không có PIL, dùng kích thước gốc
            return img
        except Exception as e:
            print(f"Lỗi load icon {icon_name}: {e}")
            return None
    
    return None


def get_icon_text(icon_name: str) -> str:
    """
    Trả về emoji fallback nếu không có icon file
    
    Args:
        icon_name: Tên icon
        
    Returns:
        Emoji string
    """
    emoji_map = {
        "app": "🔍",
        "search": "🔍",
        "user": "👤",
        "password": "🔒",
        "email": "✉",
        "invite": "⭐",
        "eye": "👁️",
        "eye_slash": "🙈",
    }
    return emoji_map.get(icon_name, "")


def create_icon_label(parent, icon_name: str, font_size: int = 16, 
                     bg_color: str = None, fg_color: str = "white") -> Label:
    """
    Tạo Label với icon (từ file hoặc emoji)
    
    Args:
        parent: Parent widget
        icon_name: Tên icon
        font_size: Kích thước font cho emoji
        bg_color: Màu nền
        fg_color: Màu chữ
        
    Returns:
        Label widget
    """
    icon_img = load_icon(icon_name, size=(font_size, font_size))
    
    if icon_img:
        # Dùng icon từ file
        label = Label(parent, image=icon_img, bg=bg_color, fg=fg_color)
        label.image = icon_img  # Giữ reference để tránh garbage collection
        return label
    else:
        # Dùng emoji fallback
        emoji_text = get_icon_text(icon_name)
        label = Label(parent, text=emoji_text, font=("Arial", font_size), 
                     bg=bg_color, fg=fg_color)
        return label

